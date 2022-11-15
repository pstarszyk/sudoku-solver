# sudoku-solver

`sudoku-solver` is an app that takes an image of your sudoku board and outputs an image of your board with the solution overlayed.

![](https://github.com/pstarszyk/sudoku-solver/blob/main/docs/gifs/solver.gif)

# Run the App

First run the following to clone repo and build image

```
git clone git@github.com:pstarszyk/sudoku-solver.git
cd sudoku-solver
docker build -t app .
docker run -p 8001:8001 -e PORT=8001 app
```

Now your app is running and you can call endpoint `http://0.0.0.0:8001/solve`

