import bpy

def same_prop(collection,index,prop) :
    return [i for i,l in enumerate(collection) if getattr(l,prop) == getattr(collection[index],prop)]


def move_layer_up(collection,index) :
    above_layer = reversed([i for i,l in enumerate(collection) if i< index])

    new_index =  0
    for i in above_layer :
        layer = collection[i]
        if layer.type == 'LAYER' and layer.id ==-1 or layer.type == 'GROUP' :
            new_index = i
            break

    #collection.move(index,new_index)
    return new_index

def move_layer_down(collection,index):
    below_layer = [i for i,l in enumerate(collection) if i> index]

    new_index =  len(collection)-1
    for i in below_layer :
        layer = collection[i]
        same_group= same_prop(collection,i,'id')
        print('same group',same_group)
        if layer.type == 'LAYER' and layer.id ==-1  :
            print(1)
            '''
            if i == index +1 :
                new_index = i
            else :
                new_index = i-1
                '''
            new_index = i
            break

        elif layer.type == 'GROUP' and len(same_group)==1 :
            print(2)
            new_index = i
            break

        elif layer.type == 'GROUP' and collection[i-1].type =='LAYER' and collection[i-1].id !=-1 and collection[index].id!=collection[i].id:
            print(3)
            new_index = i
            break

        elif layer.type == 'LAYER' and layer.id !=-1 and layer.id == max(same_group) and collection[index].id!=collection[i].id :
            print(4)
            new_index = i
            break
        '''
            if i+i
        and collection[i+1].id == -1 or layer.type == 'GROUP' and collection[i+1].type == 'GROUP':
            new_index = i
            break
        '''




    #collection.move(index,new_index)
    return new_index

def move_group_up(collection,index) :
    for i in [i for i,l in enumerate(collection) if l.id == collection[index].id]:
        new_index = move_layer_up(collection,i)

    return new_index

def move_group_down(collection,index) :
    for i in [i for i,l in enumerate(collection) if l.id == collection[index].id]:
        new_index = move_layer_down(collection,i)
    return new_index
