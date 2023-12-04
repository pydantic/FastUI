# FastUI Demo

This a simple demo app for FastUI, it's deployed at [fastui-demo.onrender.com](https://fastui-demo.onrender.com).

## Running

To run the demo app, execute the following commands from the FastUI repo root

```bash
# create a virtual env
python3.11 -m venv env311
# activate the env
. env311/bin/activate
# install deps
make install
# run the demo server
make dev
```

Then navigate to [http://localhost:8000](http://localhost:8000)

If you want to run the dev version of the React frontend, run

```bash
npm install
npm run dev
```

This will run at [http://localhost:3000](http://localhost:3000), and connect to the backend running at `localhost:3000`.
