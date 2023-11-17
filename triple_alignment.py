def levenshtein_distance(str1, str2):
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n]

def triple_alignment(str1, str2, str3, dp):
    len1, len2, len3 = len(str1.split()), len(str2.split()), len(str3.split())

    for i in range(len1 + 1):
        for j in range(len2 + 1):
            for k in range(len3 + 1):  # Correction ici
                if i == 0 or j == 0 or k == 0:
                    dp[i][j][k] = i + j + k
                else:
                    cost = 0 if str1.split()[i - 1] == str2.split()[j - 1] == str3.split()[k - 1] else 1
                    dp[i][j][k] = min(
                        dp[i - 1][j][k] + 1,
                        dp[i][j - 1][k] + 1,
                        dp[i][j][k - 1] + 1,
                        dp[i - 1][j - 1][k - 1] + cost
                    )



    return dp


def get_triple_alignment(str1, str2, str3, dp):
    align1, align2, align3 = [], [], []
    i, j, k = len(str1.split()), len(str2.split()), len(str3.split())

    while i > 0 or j > 0 or k > 0:
        if i > 0 and dp[i][j][k] == dp[i - 1][j][k] + 1:
            align1.insert(0, str1.split()[i - 1])
            align2.insert(0, "<eps>")
            align3.insert(0, "<eps>")
            i -= 1
        elif j > 0 and dp[i][j][k] == dp[i][j - 1][k] + 1:
            align1.insert(0, "<eps>")
            align2.insert(0, str2.split()[j - 1])
            align3.insert(0, "<eps>")
            j -= 1
        elif k > 0 and dp[i][j][k] == dp[i][j][k - 1] + 1:
            align1.insert(0, "<eps>")
            align2.insert(0, "<eps>")
            align3.insert(0, str3.split()[k - 1])
            k -= 1
        else:
            align1.insert(0, str1.split()[i - 1])
            align2.insert(0, str2.split()[j - 1])
            align3.insert(0, str3.split()[k - 1])
            i -= 1
            j -= 1
            k -= 1

    # Ajouter les symboles <eps> restants
    while i > 0:
        align1.insert(0, str1.split()[i - 1])
        align2.insert(0, "<eps>")
        align3.insert(0, "<eps>")
        i -= 1
    while j > 0:
        align1.insert(0, "<eps>")
        align2.insert(0, str2.split()[j - 1])
        align3.insert(0, "<eps>")
        j -= 1
    while k > 0:
        align1.insert(0, "<eps>")
        align2.insert(0, "<eps>")
        align3.insert(0, str3.split()[k - 1])
        k -= 1

    # Supprimer les <eps> inutiles au début des alignements
    while align1[0] == "<eps>" and align2[0] == "<eps>" and align3[0] == "<eps>":
        align1.pop(0)
        align2.pop(0)
        align3.pop(0)

    return align1, align2, align3

# Exemple d'utilisation
str1 = "salut tu vas bien car pas moi"
str2 = "salu tu vax sien car pa moi"
str3 = "euh salu tu va viens car pas"

dp = [[[0] * (len(str3.split()) + 1) for _ in range(len(str2.split()) + 1)] for _ in range(len(str1.split()) + 1)]
dp = triple_alignment(str1, str2, str3, dp)  # Remplir la table de programmation dynamique

align1, align2, align3 = get_triple_alignment(str1, str2, str3, dp)

print("Alignement 1:", align1)
print("Alignement 2:", align2)
print("Alignement 3:", align3)

