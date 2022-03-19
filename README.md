Как запускать тесты? 

Делаете клон директории и кладёте `tester.py` и `test` в одну папку с тестами.

Запуск tester.py, для этого у вас должен  быть установлен python 3.7 и выше, находясь в репозитории с решением, 
в командной строке вы прописываете `python tester.py "compile_commmand" "run_command"`. Ковычки ставить обязательно.

`compile_command` в данном случае команда, с помощью которой вы компилируете свой код, пример с gcc:

`gcc main.c -o main`

`run command` - команда для запуска `.exe` файла (без названий input и output файлов), пример:
`.\main`

итого команда должна выглядить так:

Для windows:
`python tester.py "gcc main.c -o main" ".\main"`

Для MacOS: 
`python3 tester.py "gcc -o main main.c" "./main"` 
