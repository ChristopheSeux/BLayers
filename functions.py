import bpy

def same_prop(collection,index,prop) :
    return [i for i,l in enumerate(collection) if getattr(l,prop) == getattr(collection[index],prop)]

def redraw_areas():
    for area in bpy.context.screen.areas :
        area.tag_redraw()



def move_layer_up(collection,index) :

    above_layer = reversed([i for i,l in enumerate(collection) if i< index])

    new_index =  0
    for i in above_layer :
        layer = collection[i]
        if layer.type == 'LAYER' and layer.id ==-1 or layer.type == 'GROUP' :
            new_index = i
            break

    return new_index

def move_layer_down(collection,index):
    #print('active_index',collection[i].id)
    if collection[index].type == 'LAYER':
        below_layer = [i for i,l in enumerate(collection) if i> index]
    elif collection[index].type == 'GROUP':
        below_layer = [i for i,l in enumerate(collection) if i> index if l.id !=collection[index].id]

    new_index =  len(collection)-1
    for i in below_layer :
        layer = collection[i]
        same_group= same_prop(collection,i,'id')

        if layer.type == 'LAYER' and layer.id ==-1  :
            new_index = i
            break

        elif layer.type == 'GROUP' and len(same_group)==1 :
            new_index = i
            break


        elif layer.type == 'LAYER' and layer.id !=-1 and i == max(same_group):
            new_index = i
            break

    return new_index
