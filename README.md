# Сервис микроблогов

## Описание проекта

Этот проект представляет собой бэкенд для корпоративного сервиса микроблогов, аналогичного Twitter, но с урезанным
функционалом. Основная задача - реализовать API для работы с микроблогами, обеспечив возможность создания, удаления
и управления твитами, а также подписки на других пользователей и отметки "Нравится".

## Функциональные возможности

- Добавление нового твита
- Удаление своего твита
- Подписка на другого пользователя
- Отписка от другого пользователя
- Отметка твита как "Нравится"
- Удаление отметки "Нравится"
- Получение ленты твитов 
- Возможность добавления картинок к твитам

## Технические требования

- Docker: Легкое развертывание с использованием Docker Compose
- PostgreSQL: Используется как база данных для хранения информации о пользователях, твитах, лайках, подписках и медиафайлах
- Swagger: Автоматическая документация API, доступная при запуске приложения
- Unit-тесты: Покрытие кода тестами для обеспечения стабильности и корректности работы
- Линтеры: Код проверен с помощью линтеров для обеспечения высокого качества

## Установка и запуск

### Предварительные требования

- Docker
- Docker Compose

### Шаги установки
- Запуск приложения осуществляется командой docker-compose up -d
- Приложение будет доступно по адресу http://localhost:8080

## API Документация

Документация API, созданная с помощью Swagger, доступна по адресу http://localhost:8001/docs.
 
## Тестирование

Для запуска тестов выполните следующую команду: pytest tests

#### Демонстрация работы сервиса доступна по ссылке: http://alexdavyd.ru:8080/
