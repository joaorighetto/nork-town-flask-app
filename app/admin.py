from flask import redirect, url_for
from flask_admin import expose, AdminIndexView
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from wtforms import ValidationError

from app.models import Car


class CustomAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', user=current_user)
    
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


class BaseAdminView(ModelView):
    can_view_details = True
    create_modal = True
    edit_modal = True
    
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
    

class CarAdminView(BaseAdminView):
    column_list = ('id', 'model', 'color', 'owner_id', 'owner.name')
    column_details_list = ('id', 'model', 'color', 'owner_id', 'owner.name')
    column_labels = {
        'id': 'ID',
        'model': 'Car Model',
        'color': 'Car Color',
        'owner_id': 'Owner ID',
        'owner.name': 'Owner Name'
    }
    form_columns = ('model', 'color', 'owner_id')  
    
    def validate_owner_car_limit(self, form, field):
        owner_id = field.data
        car_count = Car.query.filter_by(owner_id=owner_id).count()
        if car_count >= 3:
            raise ValidationError('An owner cannot have more than 3 cars.')
        
    def on_model_change(self, form, model, is_created):
        self.validate_owner_car_limit(form, form.owner_id)
        return super(CarAdminView, self).on_model_change(form, model, is_created)


class PersonAdminView(BaseAdminView):
    column_list = ('id', 'name', 'cars')
    column_details_list = ('id', 'name', 'cars')
    column_labels = {
        'id': 'ID',
        'name': 'Name',
        'cars': 'Cars'
    }
    form_excluded_columns = ('cars',)

    def _list_thumbnail(view, context, model, name):
        if not model.cars:
            return ''
        return ' // '.join([f"{car.model.name} ({car.color.name})" for car in model.cars])

    column_formatters = {
        'cars': _list_thumbnail
    }