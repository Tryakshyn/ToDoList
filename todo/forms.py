from django.forms import ModelForm

from .models import tasklist


class todo_task(ModelForm):
    class Meta:
        model = tasklist # Указываем модель, которая будет использоваться для формы
        fields = ['title','memo','important'] # Указываем поля модели, которые будут отображены в форме