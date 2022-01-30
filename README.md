# Usage
```python
python .\cliport\demos_balanced.py n=2880 task=place-obj-in-container mode=train disp=False save_data=True
```
to enable visualization, use `disp=True`. This will:
- generate 24 * 120 demos, so basically 120 demos for each of the 24 instructions

Sample output log looks like:
```bash
python .\cliport\demos_balanced.py n=2880 task=place-obj-in-container mode=train disp=False save_data=True
...
...
Total Reward: 1.000 | Done: True | Goal: place yellow hexagon into green bowl
Done episode: 2878
Oracle demo: 2879/2880 | Seed: 126
Total Reward: 1.000 | Done: True | Goal: place yellow hexagon into green bowl
Done episode: 2879
Oracle demo: 2880/2880 | Seed: 126
Total Reward: 1.000 | Done: True | Goal: place yellow hexagon into green bowl
Done episode: 2880
Collected: {'place red block into green box', 'place red block into green bowl', 'place green hexagon into green box', 'place yellow block into red bowl', 'place yellow hexagon into red bowl', 'place yellow block into green bowl', 'place green block into red bowl', 'place green hexagon into green bowl', 'place red block into red bowl', 'place green block into green box', 'place red block into red box', 'place green block into green bowl', 'place green block into red box', 'place yellow block into red box', 'place red hexagon into red bowl', 'place red hexagon into green box', 'place green hexagon into red bowl', 'place yellow hexagon into green box', 'place yellow hexagon into green bowl', 'place green hexagon into red box', 'place yellow hexagon into red box', 'place yellow block into green box', 'place red hexagon into red box', 'place red hexagon into green bowl'}
```