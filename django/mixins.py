from django.core.paginator import Paginator

class SlicePaginatorMixin(object):
	
	def __init__(self, *args, **kwargs):
		super(SlicePaginatorMixin, self).__init__(*args, **kwargs)
		if not hasattr(self, 'slice_count'):
			self.slice_count = 10
	
	def get_context_data(self, **kwargs):
		context = super(SlicePaginatorMixin, self).get_context_data(**kwargs)

		class SlicePaginator(Paginator): page_range = None

		page_obj = context.get('page_obj')

		if page_obj:
			current_page_num = page_obj.number
			page_range = page_obj.paginator.page_range
			start_page_num = current_page_num // self.slice_count if current_page_num % self.slice_count else current_page_num // self.slice_count - 1
			start_page_num *=self.slice_count
			end_page_num = start_page_num + self.slice_count
			new_paginator = SlicePaginator(object_list=self.get_queryset(), per_page=self.paginate_by, orphans=self.get_paginate_orphans(), allow_empty_first_page=self.get_allow_empty())
			new_paginator.page_range = page_range[start_page_num: end_page_num]
			page_obj.paginator = new_paginator
			context['page_obj'] = page_obj
			
		return context



from django.db.models import Q
from django.db import models
from six import string_types
from django.db.models.fields.files import FieldFile


class SearchFilterMixin(object):
	filter_arg_postfix = 'icontains'
	keyword_field_name = 'q'
	search_fields = tuple()

	def get_queryset(self):
		query_set = super(SearchFilterMixin, self).get_queryset()
		query = self.request.GET.get(self.keyword_field_name)
		if query:
			q = Q()
			for field in self.search_fields:
				q |= Q(**{'{}__{}'.format(field, self.filter_arg_postfix):query})
			return query_set.filter(q)
		return query_set


# DB 삭제시 파일 필드의 실제 파일도 같이 삭제, 매니저에 믹스인 하여 모델클래스에 objects로 등록
class DeleteWithFileMixin(object):
	def get_queryset(self):
		class DeleteQueryset(models.query.QuerySet):
			def delete(self, don_deletes=None):				
				for instance in self:
					for attr in instance.__dict__:
						if attr in [don_deletes] if isinstance(don_deletes, string_types) else don_deletes or []:
							continue
						field = getattr(instance, attr)
						if isinstance(field, FieldFile):
							field.delete()
				return super(DeleteQueryset, self).delete()
		return DeleteQueryset(self.model, using=self._db)