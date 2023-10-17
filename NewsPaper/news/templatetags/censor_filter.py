from django import template


register = template.Library()


censor_words = ['жидкое', 'Жидкое', 'Мост', 'мост']


class StringException(Exception):
   def __str__(self):
      return 'Принимает только строковый тип.'

@register.filter()
def censor(text):
   tx = text.split()
   for a, b in enumerate(tx):
      if b in censor_words:
         tx[a] = b[0] + '*' * int(len(b) - 1)
   # Возвращаемое функцией значение подставится в шаблон.
   return ' '.join(tx)
