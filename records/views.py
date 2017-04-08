from django.http import HttpResponse
from django.shortcuts import render
from records.models.docs import Document, DocumentAccess


def home_view(request):
    try:
        owner_id = request.user.person.id
        shard = request.user.person.shard
    except:
        return render(request, 'home.html', {'url_list': []})
    docs = Document.objects.filter(owner=owner_id)
    links = [{
        # 'url': request.build_absolute_uri('/document/' + format(shard, '06d') + '-' + format(d.id, '014d')),
        'shard': format(shard, '06d'),
        'docid': format(d.id, '014d'),
        'title': d.title,
        'date': d.created_at
        } for d in docs]
    return render(request, 'home.html', {'links': links})


def doc_view(request, shard, docid):
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
        doc_access = DocumentAccess.objects.filter(docid=docid, user=user_id).first()
        if not doc_access or doc_access.access_type != "Read":
            content = "No Access"
    return render(request, 'document.html', {'object': content})
