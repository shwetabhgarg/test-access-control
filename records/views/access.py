from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from records.models.docs import Document, PendingApprovalRequest


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
                'date': r.get('document__created_at')
            } for r in requests]
        return render(request, 'requests.html', {
            'pending_reqs': pending_reqs,
            'shard': format(request.user.person.shard, '06d')
            })


class ShareView(View):
    def get(self, request, shard, docid):
        try:
            user_id = request.user.person.id
        except:
            return HttpResponse(status=401)

        shard = int(shard)
        docid = int(docid)

        # connect to db node # shard
        owner = Document.objects.get(id=docid).owner
        if owner != user_id:
            return HttpResponse(status=403)

        return render(request, 'share.html', {
            'shard': format(request.user.person.shard, '06d'),
            'docid': format(docid, '014d')
        })
