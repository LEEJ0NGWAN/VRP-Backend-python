n = int(input())
arr = [list(map(int,input())) for _ in range(n)]
visited=[[0]*n]*n
dx = [1,-1,0,0]
dy = [0,0,1,-1]
def dfs(i,j):
    #print('{} , {}방문'.format(i,j))
    ret = 0
    global visited,dx,dy,arr,n
    for a in range(4):
        #print(a)
        nx = i+dx[a]
        ny = j+dy[a]
        if nx < 0 or ny < 0 or nx >= n or ny >= n:
            continue
        if arr[nx][ny] == 0 or visited[nx][ny] == 1:
            continue
        visited[nx][ny] = 1
        ret += dfs(nx , ny)
        #print(ret)
    return ret
ans=[]
for i in range(n):
    for j in range(n):
        #print(str(arr[i][j]), end=' ')
        if arr[i][j] == 1 and visited[i][j] == 0:
            visited[i][j]=1
            temp = dfs(i,j)
            #print(temp)
            ans.append(temp)
    print("\n")
print(len(ans))
print(*sorted(ans),sep='\n')