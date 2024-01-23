from typing import Tuple, Dict, Any
from django.views.generic import TemplateView
from elasticsearch_dsl import Q

from searching.documents import ProductDocument
from shop.models import Product
from shop.mixins import ExtraContextMixin


class ElasticsearchView(ExtraContextMixin, TemplateView):
    template_name = "shop/elasticsearch.html"

    def perform_search(self, title, category) -> Product:
        base_query = Q('bool', must=[], must_not=[])
        if title:
            title_query = Q('match', title=title)
            base_query.must.append(title_query)

        if category != 'All':
            category_query = Q('match', category=category)
            base_query.must.append(category_query)

        if base_query.must:
            return ProductDocument.search().query(base_query).to_queryset()

        return base_query.must

    def get_search_query(self) -> Tuple[str, str]:
        title = self.request.GET.get('title', None)
        category = self.request.GET.get('category', None)
        return title, category

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        search_title, search_category = self.get_search_query()
        context['my_search'] = self.perform_search(search_title, search_category)

        return context
