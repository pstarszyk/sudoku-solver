# sudoku-solver

`sudoku-solver` is an app that takes an image of your sudoku board and outputs an image of your board with the solution overlayed.

![](https://github.com/pstarszyk/sudoku-solver/blob/main/docs/gifs/solver.gif)

# Run the App

Run the following to clone repo, build and run docker image

```
git clone git@github.com:pstarszyk/sudoku-solver.git
cd sudoku-solver
docker build -t app .
docker run -p 8001:8001 -e PORT=8001 app
```

Now your app is running and you can call endpoint `http://0.0.0.0:8001/solve`

# cURL

If you have your own app in which you want to call this endpoint or you just want to call it from terminal, the below curl command sends a POST request of your image file and outputs the bytes response as JPG in your specified path. 

```
curl -X POST \
-F files=@<path/to/your/file.jpg> \
http://0.0.0.0:8001/solve \
--output <path/to/your/output.jpg>
```

![](https://github.com/pstarszyk/sudoku-solver/blob/main/docs/gifs/curl.gif)
