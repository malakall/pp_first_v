# не забыть про .env рядом с Dockerfile 
# при запуске в доккере подкл к контейнеру с беком и применить миграции и затем прочекать в контейнере бд что создались таблчики: alembic revision --autogenerate -m "add heatmaps table" и alembic upgrade head
