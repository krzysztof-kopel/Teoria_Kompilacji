# Test zagnieżdżonych struktur i NumPy
A = eye(4);
B = ones(4);
C = A .+ B;
print "Macierz startowa C:", C;

for i = 0:3 {
    for j = 0:3 {
        if (i == j) {
            C[i, j] = C[i, j] * 10;
        } else {
            C[i, j] = i + j;
        }

        if (i > 2) break; # Sprawdzenie break w zagnieżdżeniu
    }
}

print "Macierz po transformacji:";
print C;

x = 10;
while (x > 0) {
    x = x - 1;
    if (x == 5) continue;
    print "x =", x;
}