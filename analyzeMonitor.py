
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("log.csv")
df["time"] = pd.to_datetime(df["time"])


print("Number of readings:", len(df))
print("time range: ", df["time"].min(), " to ", df["time"].max())


print("CPU statistics")
print(f"average CPU: {df['cpu_percent'].mean():.2f}%")
print(f"peak CPU: {df['cpu_percent'].max():.2f}%")
peak_cpu = df.loc[df["cpu_percent"].idxmax()]
print("Peak CPU time:", peak_cpu["time"])


print("Memory statistics ")
print(f"average used memory: {df['mem_used'].mean():.2f} MiB")
print(f"peak used memory: {df['mem_used'].max():.2f} MiB")
print(f"total memory: {df['mem_total'].iloc[-1]} MiB")
peak_memory = df.loc[df["mem_used"].idxmax()]
print("Peak memory time:", peak_memory["time"])


fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

axes[0].plot(df["time"], df["cpu_percent"])
axes[0].set_title("CPU usage over time")
axes[0].set_ylabel("CPU Usage")
axes[0].grid(True)

axes[1].plot(df["time"], df["mem_used"])
axes[1].set_title("Memory usage over time")
axes[1].set_ylabel("Used Memory")
axes[1].set_xlabel("Time")
axes[1].grid(True)

plt.tight_layout()
plt.savefig("monitorAnalysis.png", dpi=150)
plt.show()
