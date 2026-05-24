import random
import graphviz

class CAg:

    def __init__(self, sf_num = 1, wl = 2, mem_len = 10):
        self.sf_num = sf_num
        self.detectors = []
        self.effectors = []
        self.values = []
        self.wl = wl
        self.mem_len = mem_len
        self.surrounding = None

    def make_word(self, n = 2):
        letters = [chr(x) for x in range(97, 97+26)]
        c = ""
        for x in range(n):
            c = c+random.choice(letters)
        return c

    def make_sf(self):
        self.detectors, self.effectors = [self.make_word(self.wl) for x in range(self.sf_num)], [self.make_word(self.wl) for x in range(self.sf_num)]
        self.values = [0 for x in range(self.sf_num)]
    
    def retrieve(self, surrounding):
        self.surrounding = [x for x in surrounding]

    def count(self):
        match_dict = {}
        k = 0
        for x in self.surrounding:
            num = self.detectors.count(x)
            if num > 0:
                ind = [i for i, e in enumerate(self.detectors) if e == x]
                match_dict[k] = ind
            k = k+1
        return match_dict        

    def check(self, match_dict):
        if match_dict == {}:
            self.adapt()
        else:
            self.respond(match_dict)

    def adapt(self):
        sel = random.choice(self.surrounding)
        if len(self.detectors) >= self.mem_len:
            ind = [i for i, e in enumerate(self.detectors) if self.values[i] == min(self.values)]
            ind = random.choice(ind)
            self.detectors[ind] = sel
            self.effectors[ind] = random.choice(self.surrounding)
            self.values[ind] = 1
        else:
            self.detectors.append(sel)
            self.effectors.append(random.choice(self.surrounding))
            self.values.append(1)
        
    def respond(self, match_dict):
        ind = random.choice(list(match_dict.keys()))
        which = random.choice(match_dict[ind])
        self.surrounding[ind] = self.effectors[which]
        self.values[which] = min(self.values[which]+1, 10)

    def remove_zero_values(self):
        for x in range(len(self.values)):
            if self.values[x] == 0:
                self.detectors[x] = "*"
                self.effectors[x] = "*"
        self.values = [x for x in self.values if x != 0]
        self.detectors = [x for x in self.detectors if x != "*"]
        self.effectors = [x for x in self.effectors if x != "*"]
    
    def get_sf(self):
        sf = []
        for x in range(len(self.detectors)):
            sf.append([self.detectors[x], self.effectors[x]])
        return sf

# PLOTTING    

    def plot_agent(self):
        dot = graphviz.Digraph(name="agent")
        d = graphviz.Digraph(name="cluster_detectors")
        for i,x in enumerate(self.detectors):
            d.node(str(i), label=str(x), style='filled',shape='box', fontcolor='white',fontname='Gill Sans')
        e = graphviz.Digraph(name="cluster_effectors")
        for i,x in enumerate(self.effectors):
            e.node(str(i+len(self.detectors)), label=str(x), style='filled',shape='box', fontname='Gill Sans' )
        for x in range(len(self.detectors)):
            dot.edge(str(x), str(x+len(self.detectors)), label=" "+str(self.values[x]), fontname='Gill Sans')
        dot.subgraph(d)
        dot.subgraph(e)
        return dot

    def plot_topology(self):
        dot = graphviz.Digraph(name="agent")
        dot.graph_attr['rankdir'] = 'LR' 
        for x in [k for k in self.detectors if k not in self.effectors]:
            dot.node(x,style='filled',shape='box', fontcolor='white',fontname='Gill Sans')
        for x in [k for k in self.effectors if k not in self.detectors]:
            dot.node(x, style='filled',shape='box', fontname='Gill Sans')
        for x in [k for k in self.effectors if k in self.detectors]:
            dot.node(x, style='filled',shape='box', fontname='Gill Sans',fontcolor='red')    
        for x in range(len(self.detectors)):
            dot.edge(self.detectors[x], self.effectors[x], fontname='Gill Sans', label=" "+str(self.values[x]))
        return dot


class Band:

    def __init__(self, n=10, wl=3, mem_len=10, sr_size=None):
        self.agents = [CAg(wl=wl, mem_len=mem_len) for x in range(n)]
        for x in self.agents:
            x.make_sf()
        if sr_size is None:
            sr_size = n
        #self.surrounding = [random.choice(x.effectors) for x in self.agents]
        self.surrounding = [self.agents[0].make_word(wl) for x in range(sr_size)]

    def turn(self):
        ag = random.choice(self.agents)
        ag.retrieve(self.surrounding)
        d = ag.count()
        ag.check(d)
        self.surrounding = [x for x in ag.surrounding]

    def remove_zero_values(self):
        for x in self.agents:
            x.remove_zero_values()

    def explode(self):
        d, e = [],[]
        for a in self.agents:
            [d.append(x) for x in a.detectors]
            [e.append(x) for x in a.effectors]
        exploded = []
        for x in range(len(d)):
            exploded.append((d[x], e[x]))
        return exploded
    
    def get_sf_dict(self):
        sf = []
        for a in self.agents:
            [sf.append(tuple(x)) for x in a.get_sf()]
        sf_s = set(sf)
        d = {}
        for x in sf_s:
            d[x] = sf.count(x)
        return d
        
# PLOTTING
    def plot_band(self, rankdir="LR", format=None):
        g = graphviz.Digraph(name="band", format=format)
        g.graph_attr['rankdir'] = rankdir 
        g.graph_attr['color'] = 'red' 
        for s in self.surrounding:
            g.node(s, style='filled',shape='note', fillcolor="darkgreen", fontcolor='white',fontname='Gill Sans')
        for i,a in enumerate(self.agents):
            g.node(str(i), label=str(i), style='filled',shape='circle', color='black', fillcolor="darkorange", fontcolor='white',fontname='Gill Sans')
        for i,a in enumerate(self.agents):
            for d in a.detectors: 
                if d in self.surrounding:
                    g.edge(d,str(i))
            for e in a.effectors:
                if e in self.surrounding:
                    g.edge(str(i), e)
        return g

    def plot_exploded(self, exploded):
        g = graphviz.Digraph()
        for x in exploded:
            g.node(x[0], style='filled',shape='box', fontcolor='red',fontname='Gill Sans')
            g.node(x[1], style='filled',shape='box', fontcolor='red',fontname='Gill Sans')
            g.edge(x[0], x[1])
        return g

    def plot_sharedness(self, sf_dict):
        g = graphviz.Digraph(engine="dot")
        g.graph_attr['rankdir'] = 'LR'
        for x in sf_dict:
            if sf_dict[x] >1:
                c = "red"
                lb = str(sf_dict[x])
            else:
                c = "black"
                lb = ""
            g.node(x[0], style='filled',shape='box', fontcolor="black",fontname='Gill Sans')
            g.node(x[1], style='filled',shape='box', fontcolor="black",fontname='Gill Sans')
            g.edge(x[0], x[1], color=c, label=lb, fontname='Gill Sans', fontcolor=c)
        return g