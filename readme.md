creating vritual env
python3 -m venv fastapi
activate virtual env
source ../fastapi/bin/activate
run the service
uvicorn main:app --reload
login github docker registry
docker login --username orttak --password github_classic_token ghcr.io
soru: endpointlere direk login yok. once login olup oradan token alip hayatimiza oyle devam ediyoruz
