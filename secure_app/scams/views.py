
from django.shortcuts import render, redirect
from .models import ScamReport, ScamEntity
from django.contrib import messages


def report_view(request):
    if request.method == 'POST':
        entity_type = request.POST.get('entity_type')
        value = request.POST.get('value')
        scam_category = request.POST.get('scam_category')
        description = request.POST.get('description')
        evidence_image = request.FILES.get('evidence_image')

        if not value or not description:
            messages.error(
                request,
                'Please fill in both value and description.'
            )

            return render(request, 'reports.html', {
                'entity_type': entity_type,
                'value': value,
                'description': description,
                'scam_category': scam_category,
            })

        entity, created = ScamEntity.objects.get_or_create(
            value=value,
            defaults={
                'entity_type': entity_type,
                'status': 'suspicious',
            },
        )

        ScamReport.objects.create(
            entity=entity,
            description=description,
            evidence_image=evidence_image,
            scam_category=scam_category,
        )

        entity.refresh_status()

        return redirect(f'/?q={value}')

    return render(request, 'reports.html')


def home_view(request):
    query=request.GET.get('q', '').strip()
    entity=None
    search_results=None
    if query:
        search_results=True  
        entity = ScamEntity.objects.filter(value__icontains=query)
    context={'query': query, 'entity': entity, 'search_result': search_results}
    return render(request, 'home.html', context)


