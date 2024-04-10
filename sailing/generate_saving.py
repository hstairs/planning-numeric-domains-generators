#!/usr/bin/python3
import sys
import os
import argparse
import math
import random
import string
from string import Template

template_name = "template.pddl"

def generate_instance(instance_name, num_boats,num_people,max_dist_goals):
    with open( template_name ) as instream :
        text = instream.read()
        template = string.Template( text )
    template_mapping = dict()
    template_mapping['instance_name'] = instance_name
    template_mapping['domain_name'] = 'sailing'
    
    people = ''
    people_distance = ''
    people_to_save = ''
    for i in range(num_people):
        people+='p'+str(i)+' '
        #d = random.randint(-max_dist_goals,max_dist_goals)
        d = random.randint(0,max_dist_goals)
        people_distance+= '(= (d p'+str(i)+') '+str(d)+')\n' 
        people_to_save+='(saved p'+str(i)+')\n'

    boats = ''
    boats_positions = ''
    for i in range(num_boats):
        boats+='b'+str(i)+' '
        x_pos = random.randint(-10,+10)
        boats_positions+= '(= (x b'+str(i)+') '+str(x_pos)+')\n(= (y b'+str(i)+') 0)\n' 
    
    template_mapping['boat_name_list'] = boats
    template_mapping['boat_positions'] = boats_positions
    template_mapping['people_name_list'] = people
    template_mapping['people_d_position'] = people_distance
    template_mapping['people_to_save'] = people_to_save    
    
    print(template.substitute(template_mapping))

def parse_arguments() :
    parser = argparse.ArgumentParser( description = "Generate sailing planning instance" )
    parser.add_argument( "--random_seed", required=False, help="Set RNG seed", default = "1229")
    parser.add_argument( "--num_instances", required=False, help="Number of instances to generate (defaults to 1)")
    parser.add_argument( "--num_people", required=True, help="Number of people to save" )
    parser.add_argument( "--num_boats", required=True, help="Number of boats involved" )
    parser.add_argument( "--max_dist_goals", required=False, help="Max distance people to be rescued", default = 500)

    args = parser.parse_args()
    args.random_seed = int(args.random_seed)
    if args.random_seed != None:
        random.seed( args.random_seed )
        print( ";;Setting seed to {0}".format(args.random_seed) )
    return args

def Main() :
    args = parse_arguments()
    generate_instance('instance_'+str(args.num_boats)+'_'+str(args.num_people)+'_'+str(args.random_seed),int(args.num_boats),int(args.num_people),int(args.max_dist_goals))

if __name__ == '__main__' :
    Main()
