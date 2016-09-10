# Структура объекта

                                    n0000
                                  /       \
                              n0001       n0002
                            /       \
                        n0003       n0004
                                  /   |   \
                              n0005  n0006  n0007
#На сервере созданно 2 баззы данных "measurements" и "family" они содержат следующие таблици:

family=# \d

            List of relations
            
 Schema |     Name     | Type  |  Owner  
 
--------+--------------+-------+----------

 
 public | n0000        | table | postgres
 
 public | n0001        | table | postgres
 
 public | n0002        | table | postgres
 
 public | n0003        | table | postgres
 
 public | n0004        | table | postgres
 
 public | n0005        | table | postgres
 
 public | n0006        | table | postgres
 
 public | n0007        | table | postgres
 
(8 rows)

measurements=# \d

         List of relations
         
 Schema | Name  | Type  |  Owner  
 
--------+-------+-------+----------

 public | n0000 | table | postgres
 
 public | n0001 | table | postgres
 
 public | n0002 | table | postgres
 
 public | n0003 | table | postgres
 
 public | n0004 | table | postgres
 
 public | n0005 | table | postgres
 
 public | n0006 | table | postgres
 
 public | n0007 | table | postgres
 
(8 rows)

#Выглидят они следующим образом:

measurements=# select * from n0000;

 time | temperature 
 
------+-------------

(0 rows)

family=# select * from n0000;

 id | child | capacity |   name  
 
----+-------+----------+----------

  0 | n0001 |        6 | Корпус 1
  
  1 | n0002 |        6 | Корпус 2
  
(2 rows)

Такая структура позволяет удобно раздавать пользователям правила доступа, скрыть структуру объета от лишних глаз, локализовать данные об одном объекте физически рядом ...

##В данный момент таблици измерений пусты, я предлогаю заполнять их следующим образом:

0) ip адрес сервера указан в const.py , настроил переадресацию, открыл порт, разрешил логиниться в postgres с любого ip. если не подключается, позвоните мне я проверю работает ли ноут и запушен ли сервер.

1) запустить скрипт fill_measurements.py , он выберет бездетные объекты и для каждого из них заполнит таблицу первыми N(первая строка csv файла) измерениями из соответствующего файла.

2)в скрипте fill_measurements.py разкоментировать строчки 7,77. И закоментировать строчку 75. У величить N  в csv файлах на 1. Запустить скрипт. Убедиться, что для в таблицах измерений для без детных объектов добавленна еще одно строчка

3) в скрипте fill_measurements.py разкоментировать строчку 79. У величить N  в csv файлах на 1. Запустить скрипт. Убедиться, что для объектов с детьми появилас строчка измерений посчитанная из данных их детей, с учетом их емкости.

4) в скрипте time_termo_graph.py в строчке 58 указать для какого объекта необходимо построить график, в строчке 59 иказать время начало построения(проветить что есть данные после этого времени). Запистить скрипт, нарисуются измеренные точки и их интерполяция ( не используемая функция в этом скрипте умее проводить интерполяция через измеренные точки, но она не так красиво сглаживает)

5)запустите скрипт recreate_measurements_db.py что бы почистить данные об измерениях  после себя


