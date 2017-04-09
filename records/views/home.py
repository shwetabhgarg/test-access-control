from django.shortcuts import render
from django.views.generic import View
from records.models.docs import Document, PendingApprovalRequest


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