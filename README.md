# LegacyChecker

###ТЗ
Написать одностраничное приложение, которое при POST запросе проверяет, является ли
переданный ОГРН или ИНН субъектом малого или среднего предпринимательства на
сайте https://rmsp.nalog.ru/, сохранить результат проверки. При GET запросе показать
результаты предыдущих проверок.
Требования
* ОГРН или ИНН вводится в одно поле, при вводе автоматически определять и выводить
что это - ИНН или ОГРН (реализовать на JS)
* Если проверка с введенными данными осуществлялась меньше, чем 5 минут назад -
выводить результат предыдущей проверки.

###Запуск
```
docker-compose up
```
http://localhost:5000/index - UI

http://localhost:5000/ - Swagger