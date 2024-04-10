# To change this license    header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
#!/usr/bin/python3
import networkx as nx
import matplotlib.pyplot as plt
import sys
import os
import argparse
import math
import random
import string
from string import Template

template_name = "template.pddl"

def generate_instance(instance_name, num_farms,num_units,graph_generator):
    with open( template_name ) as instream :
        text = instream.read()
        template = string.Template( text )
    template_mapping = dict()
    template_mapping['instance_name'] = instance_name
    template_mapping['domain_name'] = 'farmland'
    
    if graph_generator == 'star':
        G = nx.star_graph(num_farms-1)#,seed=1229)
    elif graph_generator == 'strogaz':
        G = nx.connected_watts_strogatz_graph(num_farms,k=min(2,num_farms-1),tries=10000,p=0.5)
    else:
        #G = nx.scale_free_graph(num_farms,alpha = 0.05,beta = 0.9,gamma = 0.05,seed=1229)
        G = nx.ladder_graph(int((num_farms)/2))
    farms = ''
    adj=''
    farms_init=''
    farms_final=''
    overall_reward_bound = '(>= '
    source = random.randint(0,num_farms-1)
    for i in range(num_farms):
        farms+='farm'+str(i)+' '
        if (i != source):
            farms_init+='(= (x farm'+str(i)+') '+str(random.randint(0,1))+')\n\t\t'
            w = "{0:.1f}".format(random.random()+1.0)
            overall_reward_bound+='(+ (* '+str(w)+' (x farm'+str(i)+'))'
        else:
            farms_init+='(= (x farm'+str(i)+') '+str(num_units)+')\n\t\t'
            w = 1.0
            overall_reward_bound+='(+ (* '+str(w)+' (x farm'+str(i)+'))'
        farms_final+='(>= (x farm'+str(i)+') 1)\n\t\t\t'
        for ele in G[i]:
            #print(i," to ",ele)
            adj+='(adj farm'+str(i)+' farm'+str(ele)+')\n\t\t'
    overall_reward_bound+=' 0'
    for i in range(num_farms):
        overall_reward_bound+=')'
    overall_reward_bound+=' '+str(num_units*1.4)+')'
    template_mapping['farm_name_list'] = farms
    template_mapping['farm_init_allocation'] = farms_init
    template_mapping['farm_connections'] = adj
    template_mapping['farm_final_requirement'] = farms_final
    template_mapping['overall_reward_bound'] = overall_reward_bound    
    
    print(template.substitute(template_mapping))

def parse_arguments() :
    parser = argparse.ArgumentParser( description = "Generate farmland planning instance" )
    parser.add_argument( "--random_seed", required=False, help="Set RNG seed", default = "1229")
    #parser.add_argument( "--num_instances", required=False, help="Number of instances to generate (defaults to 1)")
    parser.add_argument( "--num_farms", required=True, help="Number of farms" )
    parser.add_argument( "--num_units", required=True, help="Maximum Number of Units" )
    parser.add_argument( "--graph_generator", required=False, help="Graph Generator between star (default) or strogatz or ladder", default="star" )

    

    args = parser.parse_args()
    args.random_seed = int(args.random_seed)
    if args.random_seed != None:
        random.seed( args.random_seed )
        print( ";;Setting seed to {0}".format(args.random_seed) )
    return args

def Main() :
    args = parse_arguments()
    generate_instance('instance_'+str(args.num_farms)+'_'+str(args.num_units)+'_'+str(args.random_seed)+'_'+str(args.graph_generator),int(args.num_farms),int(args.num_units),args.graph_generator)

if __name__ == '__main__' :
    Main()
