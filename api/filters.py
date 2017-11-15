from rest_framework import filters

class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Return only objects owned by the current user
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user.id)

class ObjectOverlapFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        '''
        objects_{object_name}=1,2,3
        '''
        for key,value in request.GET.items():
            if key.startswith('objects_'):
                object_name = key.split('_')[1]
                values = ['{}:{}'.format(object_name, id) for id in value.split(',')]
                query = {
                    'object_ids__overlap': values
                }
                queryset = queryset.filter(**query)
        return queryset
