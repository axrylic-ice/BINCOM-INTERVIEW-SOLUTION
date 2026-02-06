from bs4 import BeautifulSoup
import random
import psycopg2  

# HTML input
html_doc = """<!DOCTYPE html>
<html>
<head>
<title>Our Python Class exam</title>
</head>
<style type="text/css">
	
	body{
		width:1000px;
		margin: auto;
	}
	table,tr,td{
		border:solid;
		padding: 5px;
	}
	table{
		border-collapse: collapse;
		width:100%;
	}
	h3{
		font-size: 25px;
		color:green;
		text-align: center;
		margin-top: 100px;
	}
	p{
		font-size: 18px;
		font-weight: bold;
	}
</style>
<body>
<h3>TABLE SHOWING COLOURS OF DRESS BY WORKERS AT BINCOM ICT FOR THE WEEK</h3>
<table>
	<thead>
		<th>DAY</th><th>COLOURS</th>
	</thead>
	<tbody>
	<tr>
		<td>MONDAY</td>
		<td>GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN</td>
	</tr>
	<tr>
		<td>TUESDAY</td>
		<td>ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLEW, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE</td>
	</tr>
	<tr>
		<td>WEDNESDAY</td>
		<td>GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE</td>
	</tr>
	<tr>
		<td>THURSDAY</td>
		<td>BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN</td>
	</tr>
	<tr>
		<td>FRIDAY</td>
		<td>GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE</td>
	</tr>
	</tbody>
</table>
</body>
</html>"""

soup = BeautifulSoup(html_doc, "html.parser")

colors_worn = []
rows = soup.find_all("tr")

for row in rows[1:]:
    cols = row.find_all("td")
    if len(cols) == 2:
        _, colors = cols
        color_list = [c.strip().upper() for c in colors.text.split(",")]
        colors_worn.extend(color_list)

# Fix typos
color_corrections = {"BLEW": "BLUE", "ARSH": "ASH"}
colors_worn = [color_corrections.get(c, c) for c in colors_worn]

# counter to manage the frequency
def counter(lst):
    colors = {}
    for i in lst:
        colors[i] = colors.get(i, 0) + 1
    return colors

def mean_color(color):
    freq = counter(color)
    mean_val = sum(freq.values()) / len(freq)
    # find color whose frequency is closest to the mean
    return min(freq.items(), key=lambda x: abs(x[1] - mean_val))[0]

def mode_color(color):
    # same as mean (mode is most frequent)
    freq = counter(color)
    return max(freq, key=freq.get)

def median_color(color):
    freq = sorted(counter(color).items(), key=lambda x: x[1])
    mid = len(freq) // 2
    if len(freq) % 2 == 1:
        return freq[mid][0]
    else:
        return (freq[mid - 1][0], freq[mid][0])

def variance(color):
    freq = list(counter(color).values())
    mean_val = sum(freq) / len(freq)
    return sum((x - mean_val) ** 2 for x in freq) / len(freq)

def prb_red(color):
    return color.count("RED") / len(color)

def psgre(color):
    # Save to PostgreSQL 
    freq = counter(color)
    try:
        conn = psycopg2.connect(
            dbname="bincom_db",
            user="postgres",
            password="yourpassword",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS color_frequency (
                id SERIAL PRIMARY KEY,
                color VARCHAR(50),
                frequency INT
            );
        """)
        cur.execute("DELETE FROM color_frequency;")
        for c, f in freq.items():
            cur.execute("INSERT INTO color_frequency (color, frequency) VALUES (%s, %s);", (c, f))
        conn.commit()
        cur.close()
        conn.close()
        return " Saved to PostgreSQL"
    except Exception as e:
        return f" DB Error: {e}"
 # CREATE A RECURSIVE SEARCH ALGORITHM
def rec_search(lst, target, idx=0):
    if idx >= len(lst):
        return -1
    if lst[idx] == target:
        return idx
    return rec_search(lst, target, idx+1)
 # GENERATE RANDOM 4 DIGIT BINARY NUMBERS AND CONVERT THEM TO BASE 10
def gen_rd_bin():
    binary = "".join(random.choice("01") for _ in range(4))
    decimal = int(binary, 2)
    return binary, decimal
 #      SUM FIRST 50 FIBONACCI NUMBERS
def sum_fib(n=50):
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a+b
    return total



#ANSWERS

print("Total colors:", len(colors_worn))
print("Mean Color:", mean_color(colors_worn))
print("Most Worn Color:", mode_color(colors_worn))
print("Median Color:", median_color(colors_worn))
print("Variance of Colors:", variance(colors_worn))
print("Probability of Red:", prb_red(colors_worn))

binary, decimal = gen_rd_bin()
print(f"Random binary: {binary}, Decimal: {decimal}")
print("Sum of first 50 Fibonacci numbers:", sum_fib())



