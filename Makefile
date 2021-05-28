docker-build:
	docker-compose -f docker/docker-compose-dev.yml build
	
docker-up:
	docker-compose -f docker/docker-compose-dev.yml up -d

docker-down:
	docker-compose -f docker/docker-compose-dev.yml down -v

docker-clean:
	docker system prune -a --volumes -f

download-requirements:
	pip install -r requirements-dev.txt

download-resources-asr:
	wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.tflite -P asr/resources/deepspeech/
	wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer -P asr/resources/deepspeech/