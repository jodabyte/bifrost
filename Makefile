build:
	docker build -f bifrost/asr/Dockerfile -t bifrost/asr:latest .

run:
	docker run --privileged --device /dev/snd:/dev/snd -v $$PWD/configs:/bifrost/configs -v $$PWD/resources:/bifrost/resources -v $$PWD/logs:/bifrost/logs bifrost/asr:latest

clean-docker:
	docker system prune -a -f --volumes