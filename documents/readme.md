creating vritual env
python3 -m venv fastapi
activate virtual env
source ./fastapi/bin/activate
run the service
uvicorn main:app --reload

soru: endpointlere direk login yok. once login olup oradan token alip hayatimiza oyle devam ediyoruz

## Defining Envrinment Variables

## Database Migration

1- initlaize alembic: alembic init alembic
2- edit alembic env.py file with your credential
3- alembic revision -m "create post table" # create migration file
we have upgrade and downgrade functions in migration file. it is like git commit.
4- after that we define upgrade and downgrade functions in migration file.
5- alembic upgrade revisionID # run migration file
6- alembci currten # show current revision. if you create new revision file and do not apply it with upgrade you can alembic upgrade head and latest changes apply to database.
7- if you also define downgrade function in migration file you can downgrade your database with alembic downgrade revisionID. if you do not define downgrade function you can not downgrade your database.

Alembic sifirdan baslamaya gerek yok. Current DB de olanlari alip migration file olusturabiliriz. Bunun icin: alembic revision --autogenerate -m "create post table"

Bu sayede direk migration file olusturulur. Bu migration file da upgrade ve downgrade fonksiyonlari olusturulur. Bu fonksiyonlarin icine de DB de olanlari yazilir. Boylece migration file olusturulmus olur.

models.py da yapialn degisiklik DB ye yansidigi anda alembic revision --autogenerate -m "unique name", alembic bu degisikligi anlayip, yeni revision dosyasi olusturu. Daha sonra alembic revision head ile alembic'i latest version a yukseltiriz. Bu sayede DB deki degisiklikler migration file a yansir.

models.Base.metadata.create_all(bind=engine)
Bu kodu main.py da yazdigimizda DB ye direk models.py da olan degisiklikler yansir. tutorial kapsaminda alembic olmadan basladigimiz icin bu script bizim icin onemli ama normalde kaldirabiliriz. Bir projeye baslarken direk alembic kismini initialize edip, migration file olusturup, DB ye yansitmak daha mantikli olur. yada olabilir

## TESTING

If we create our test scnerio in dev db, object which is created by ptest will be in dev db. So we need to create test db and test object will be in test db. Whenever we run test, test db will be created and after test db will be deleted.

## Publish Docker in Github

docker login --username orttak --password XXX ghcr.io
docker image ls
docker -t ligfinder_refactor_api:latest ghcr.io/orttak/apitest:fromlocal
docker tag ligfinder_refactor_api:latest ghcr.io/orttak/apitest:fromlocal
docker push ghcr.io/orttak/apitest:fromlocal
