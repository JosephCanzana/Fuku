.PHONY: watch-tailwind build-tailwind	
watch-tailwind:
	./theme/tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
build-tailwind:
	./theme/tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify