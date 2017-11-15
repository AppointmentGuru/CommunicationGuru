
class CurrentUserDefaultUserId(object):
    def set_context(self, serializer_field):
        self.user = serializer_field.context['request'].user

    def __call__(self):
        if self.user is not None:
            return self.user.id
        return None

    def __repr__(self):
        return unicode_to_repr('%s()' % self.__class__.__name__)
