#include <cstdio>
#include <iostream>
#include <algorithm>
using namespace std;
#define ll long long
const int N=1e5+11;
struct Edge {
	int next,to;
} edge[N<<1];
int num_edge,head[N];
int n,m;

/*
cnt = 第二次dfs当前映射的编号
dep(x) = x节点深度
fa(x) = x节点父亲
son(x) = x节点的重儿子
size(x) = x节点的大小
num(x) = x节点输入的原始值
id(x) = x的第二次编号
val(x) = x在新编号下对应的原节点
top(x) = x节点所在链的顶端


*/


int cnt,dep[N],fa[N],son[N],size[N],num[N];
int val[N],id[N],top[N];
ll res;
struct seg {
	seg *ls, *rs;
	ll sum, add, len;
#define Len (1 << 16)
	inline void* operator new(size_t) {
		static seg *mempool, *c;
		if (mempool == c)
			mempool = (c = new seg[Len]) + Len;
		c -> ls = c -> rs = NULL;
		c -> sum = c -> add = c -> len = 0;
		return c++;
	}
#undef Len

	inline void update() {
		sum = ls -> sum + rs -> sum;
	}
	inline void push() {
		ls -> sum += add * ls -> len, rs -> sum += add * rs -> len;
		ls -> add += add, rs -> add += add;
		add = 0;
	}

#define mid (l + r >> 1)
	void build(int l, int r) {
		if (l == r) {
			sum = num[val[l]];
			add = 0;
			len = 1;
			return;
		}
		(ls = new seg) -> build(l, mid);
		(rs = new seg) -> build(mid + 1, r);
		add = 0;
		len = r - l + 1;
		update();
	}

	void modify(int l, int r, int L, int R, ll del) {
		if (L <= l && r <= R) {
			add += del;
			sum += len * del;
			return;
		}
		push();
		if (L <= mid) ls -> modify(l, mid, L, R, del);
		if (mid < R) rs -> modify(mid + 1, r, L, R, del);
		update();
	}

	ll query(int l, int r, int L, int R) {
		if (L <= l && r <= R) return sum;
		push();
		ll res = 0;
		if (L <= mid) res += ls -> query(l, mid, L, R);
		if (mid < R) res += rs -> query(mid + 1, r, L, R);
		update();
		return res;
	}
#undef mid
} *T;
void adde(int from,int to) {
	edge[++num_edge].next=head[from];
	edge[num_edge].to=to;
	head[from]=num_edge;
}
void dfs1(int u,int f) {
	dep[u]=dep[f]+1;
	fa[u]=f;
	size[u]=1;
	for(int i=head[u]; i; i=edge[i].next) {
		int &v=edge[i].to;
		if(v==f)
			continue;
		dfs1(v,u);
		size[u]+=size[v];
		if(size[v]>size[son[u]])
			son[u]=v;
	}
}
void dfs2(int u,int tp) {
	id[u]=++cnt;
	val[cnt]=u;
	top[u]=tp;
	if(!son[u])
		return;
	dfs2(son[u],tp);
	for(int i=head[u]; i; i=edge[i].next) {
		int &v=edge[i].to;
		if(id[v])
			continue;
		dfs2(v,v);
	}
	return;
}

inline ll ask(int x,int y) {

	ll ans=0ll;
	while(top[x]!=top[y]) {
		if(dep[top[x]]<dep[top[y]])
			swap(x,y);
		res=0;
		res+= T-> query(1,n,id[top[x]],id[x]);
		ans+=res;
		x=fa[top[x]];
	}
	if(dep[x]>dep[y])
		swap(x,y);
	res=0;
	res+= T->query(1,n,id[x],id[y]);

	ans+=res;
	return ans;
}
int main() {
	T=new seg;
	cin>>n>>m;
	for(int i=1; i<=n; ++i)
		cin>>(num[i]);
	for(  int i=1,x,y; i<n; ++i) {
		cin>>x>>y;
		adde(x,y);
		adde(y,x);
	}
	dfs1(1,0);
	dfs2(1,1);

	T->build(1,n);
	for(int i=1,opt,x,y; i<=m; ++i) {
		cin>>(opt);
		if(opt==1) {
			cin>>x>>y;
			T->modify(1,n,id[x],id[x],y);
		} else if(opt==2) {
			cin>>x>>y;
			T->modify(1,n,id[x],id[x]+size[x]-1,y);
		} else if(opt==3) {
			cin>>x;
			printf("%lld\n",ask(1,x));
		}
	}
	return 0;
}
