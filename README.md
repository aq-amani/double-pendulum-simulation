# About this project
A script to create simulation animation of a specific number of double pendulums with a specific error in initial conditions.

## Example output

<p align="center">
  <img src="./readme_images/pendulum.gif" width="400" />
</p>

## :hammer_and_wrench: Setup/ Preparation
```bash
pipenv install --ignore-pipfile --skip-lock --python 3.9
pipenv shell
```
If faced by `UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.`
```bash
sudo apt-get install python3.9-tk
```

## :rocket: Usage examples:

#### Script options
```bash
python double-pendulum.py -h

  -h, --help     show this help message and exit
  -n , --count   Pendulum count
  -d , --delta   Initial condition delta
  -v, --video    Create a video file of the animation
  -t , --time    Number of seconds to simulate
```

#### Simulate 5 double pendulums up to 10 seconds with a 0.01 error in the angle initial condition
```bash
python double-pendulum.py -n 5 -d 0.01 -t 10
```
#### Create an mp4 video file of the case above
```bash
python double-pendulum.py -n 5 -d 0.01 -t 10 -v
```
