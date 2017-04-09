from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from records.models.docs import Document, DocumentPermission,\
    PendingApprovalRequest


class DocumentView(View):
    def get(self, request, shard, docid):
        try:
            user_id = request.user.person.id
        except:
            return HttpResponse(status=401)

        shard = int(shard)
        docid = int(docid)

        shard_db = 'shard' + str(shard)
        doc = Document.objects.using(shard_db).get(id=docid)
        if doc is None:
            return HttpResponse(status=404)
        content = doc.data
        if doc.owner != user_id:
            doc_access = DocumentPermission.objects.using(shard_db).select_related('access_type')
            doc_access = doc_access.filter(document_id=docid, user=user_id).first()
            if not doc_access or doc_access.access_type.name.lower() != "read":
                defaults = {
                    'owner': doc.owner,
                    'active': True
                }
                PendingApprovalRequest.objects.using(shard_db).update_or_create(document_id=docid,
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
            requester = int(requester)
        except:
            return HttpResponse(status=400)

        shard_db = 'shard' + str(shard)
        doc = Document.objects.using(shard_db).get(id=docid)
        if doc is None:
            return HttpResponse(status=404)
        if doc.owner != user_id:
            return HttpResponse(status=403)

        pending_req = PendingApprovalRequest.objects.using(shard_db).filter(document_id=docid, requester=requester, active=True)
        if not approval:
            pending_req.update(active=False)
        else:
            defaults = {
                'access_type_id': 1
            }
            with transaction.atomic():
                pending_req.update(active=False)
                DocumentPermission.objects.using(shard_db).update_or_create(document_id=docid,
                                                                            user=requester,
                                                                            defaults=defaults)
        return redirect('home')
