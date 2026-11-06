# Notes

## 2026-11-05 to 2026-11-06

### pyproject.toml and uv
- `pyproject.toml` has top-level headers like `[project]` and `[build-system]`. These are called **tables**, and the entries under them are **keys** with values (for example `name = "fuku"`). They aren't variables like in a typical programming language.
- Each key has its own purpose. `[build-system]` is for Python projects that get built and distributed, and its `requires` key lists the build backend (I used `hatchling`).
- I added it at first, but after reading about it I found I didn't need it. Fuku is a web app that runs from its own folder, so nothing needs to be built or installed as a package.

### Docker
- I learned how to set up and read a Dockerfile and a compose file. The Dockerfile has 7 main instructions, which I wrote in a cheat sheet. The compose file is like `pyproject.toml`: it also has headers, keys, and values, and I'm more familiar with the structure now.
- `0.0.0.0` is needed when running the server in a container so the app can be reached from outside the container.
- I also learned about env variables, volumes, and some more syntax.