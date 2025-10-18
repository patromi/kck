import pandas as pd
import matplotlib.pyplot as plt

files = ["1ers.csv","1crs.csv","2crs.csv","1c.csv", "2c.csv"]

pd_files = []

fig, axs = plt.subplots(1, 2, figsize=(14, 6))

markers = ["o","v","D","s","^"]
colors = ["b","orange","g","r","m"]

ax2 = axs[0].twinx()

for ind,file_name in enumerate(files):
    df = pd.read_csv(f"src/{file_name}")
    run_keys = df.filter(like='run-').columns
    temp_df = pd.DataFrame({
        'generation': df['generation'],
        'effort': df['effort'],
        "avg": df[run_keys].mean(axis=1)
    })
    pd_files.append((temp_df,file_name))
    axs[0].plot(temp_df['effort'], temp_df["avg"], label=file_name)

    for number in range(1,max(temp_df["generation"])+1,25):
        gen_df = temp_df[temp_df['generation'] == number]
        axs[0].scatter(gen_df["effort"], gen_df["avg"], label=gen_df["generation"].values[0],
                      marker=markers[ind], s=50, color=colors[ind], edgecolors='black')



ax2.set_ylabel("Pokolenie")
ax2.set_ylim(0, max(df['generation']) + 5)
ax2.set_yticks(range(0, max(df['generation']) + 5, 20))
axs[0].set_xlabel("Rozegranych gier")
axs[0].set_ylabel("Odsetek wygranych gier")
axs[0].grid(True)



box_data = [tup[0]["avg"].dropna().values for tup in pd_files]
box_labels = [tup[1] for tup in pd_files]

axs[1].clear()
bp = axs[1].boxplot(
    box_data,
    labels=box_labels,
    patch_artist=True,
    showmeans=True,
    meanprops={'marker': 'o', 'markerfacecolor': 'black', 'markeredgecolor': 'black'},
    medianprops={'color': 'red', 'linewidth': 2},
    capprops={'color': 'blue'},
    whiskerprops={"linestyle":"dashed",'color': 'blue'},
    boxprops={'facecolor': 'None', 'color': 'blue'},
    flierprops={'marker': '+', 'markerfacecolor': 'blue', 'markeredgecolor': 'blue', 'markersize':7}
)

axs[1].set_ylabel("Odsetek wygranych gier")
axs[1].tick_params(axis='x', rotation=25)

plt.tight_layout()
plt.show()
