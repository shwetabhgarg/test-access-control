from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from records.models.docs import Document, DocumentPermission,\
    PendingApprovalRequest


class HomeView(View):
    def get(self, request):
        # check if user maps to a person
        try:
            owner_id = request.user.person.id
            shard = request.user.person.shard
        except:
            links = []
            pending_reqs = 0
        else:
            # connect to db node # shard
            docs = Document.objects.filter(owner=owner_id)
            links = [{
                'shard': format(shard, '06d'),
                'docid': format(d.id, '014d'),
                'title': d.title,
                'date': d.created_at
                } for d in docs]
            pending_reqs = PendingApprovalRequest.objects
            pending_reqs = pending_reqs.filter(owner=owner_id, active=True).count()

        return render(request, 'home.html', {
            'links': links, 'pending_reqs': pending_reqs
            })


class ApprovalRequestsView(View):
    def get(self, request):
        # check if user maps to a person
        try:
            owner_id = request.user.person.id
        except:
            pending_reqs = []
        else:
            # connect to db node # shard
            requests = PendingApprovalRequest.objects.select_related('document')
            requests = requests.filter(owner=owner_id, active=True)
            requests = requests.values('requester', 'document_id',
                                       'document__title', 'document__created_at')
            pending_reqs = [{
                'requester': r.get('requester'),
                'docid': format(r.get('document_id'), '014d'),
                'title': r.get('document__title'),
                'date': r.get('document__created_at'),
                'shard': format(request.user.person.shard, '06d')
            } for r in requests]
        return render(request, 'requests.html', {'pending_reqs': pending_reqs})


class DocumentView(View):
    def get(self, request, shard, docid):
        try:
            user_id = request.user.person.id
        except:
            return HttpResponse(status=401)

        shard = int(shard)
        docid = int(docid)

        # connect to db node # shard
        doc = Document.objects.get(id=docid)
        if doc is None:
            return HttpResponse(status=404)
        content = doc.data
        if doc.owner != user_id:
            doc_access = DocumentPermission.objects.select_related('access_type')
            doc_access = doc_access.filter(document_id=docid, user=user_id).first()
            if not doc_access or doc_access.access_type.name.lower() != "read":
                defaults = {
                    'owner': doc.owner,
                    'active': True
                }
                PendingApprovalRequest.objects.update_or_create(document_id=docid,
                                                                requester=user_id,
                                                                defaults=defaults)
                content = "Access denied. Click here to request for access. \
                Dev shortcut: assuming user clicked on it. Request has been added\
                and is pending approval."
        return render(request, 'document.html', {'object': content})

    def post(self, request, shard, docid):
        try:
            user_id = request.user.person.id
        except:
            return HttpResponse(status=401)

        shard = int(shard)
        docid = int(docid)
        requester = request.POST.get('requester')
        approval = request.POST.get('approval')
        if requester is None or approval is None:
            return HttpResponse(status=400)
        try:
            approval = int(approval)
        except:
            return HttpResponse(status=400)

        # connect to db node # shard
        owner = Document.objects.get(id=docid).owner
        if owner != user_id:
            return HttpResponse(status=403)
        request = PendingApprovalRequest.objects.filter(document_id=docid, requester=requester, active=True)
        if not approval:
            request.update(active=False)
        else:
            defaults = {
                'access_type_id': 1
            }
            with transaction.atomic():
                request.update(active=False)
                DocumentPermission.objects.update_or_create(document_id=docid,
                                                            user=requester,
                                                            defaults=defaults)
        return redirect('home')
