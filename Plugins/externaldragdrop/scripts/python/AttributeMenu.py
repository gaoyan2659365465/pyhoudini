import hou

def point(node_relative_path):
    node = hou.pwd()
    input_node = node.node(node_relative_path)
    geo = input_node.geometry()
    final_list = []

    if geo:
        point_attrs_tuple = geo.pointAttribs()
        for point_attr in point_attrs_tuple:
            point_attr_name = point_attr.name()
            final_list.append(point_attr_name)
            final_list.append(point_attr_name)

    return final_list

def vertex(node_relative_path):
    node = hou.pwd()
    input_node = node.node(node_relative_path)
    geo = input_node.geometry()
    final_list = []

    if geo:
        vertex_attrs_tuple = geo.vertexAttribs()
        for vertex_attr in vertex_attrs_tuple:
            vertex_attr_name = vertex_attr.name()
            final_list.append(vertex_attr_name)
            final_list.append(vertex_attr_name)

    return final_list

def prim(node_relative_path):
    node = hou.pwd()
    input_node = node.node(node_relative_path)
    geo = input_node.geometry()
    final_list = []

    if geo:
        prim_attrs_tuple = geo.primAttribs()
        for prim_attr in prim_attrs_tuple:
            prim_attr_name = prim_attr.name()
            final_list.append(prim_attr_name)
            final_list.append(prim_attr_name)

    return final_list

def detail(node_relative_path):
    node = hou.pwd()
    input_node = node.node(node_relative_path)
    geo = input_node.geometry()
    final_list = []

    if geo:
        global_attrs_tuple = geo.globalAttribs()
        for global_attr in global_attrs_tuple:
            global_attr_name = global_attr.name()
            final_list.append(global_attr_name)
            final_list.append(global_attr_name)

    return final_list

#############################################################################

def vertexVector(node_relative_path):
    node = hou.pwd()
    input_node = node.node(node_relative_path)
    geo = input_node.geometry()
    final_list = []

    if geo:
        vertex_attrs_tuple = geo.vertexAttribs()
        vertex_vector_attrs_list = []

        for vertex_attr in vertex_attrs_tuple:
            if vertex_attr.size() == 3 and not vertex_attr.isArrayType():
                name = vertex_attr.name()
                vertex_vector_attrs_list.append(name)

        vertex_vector_attrs_list.sort()

        for attr_name in vertex_vector_attrs_list:
            final_list.append(attr_name)
            final_list.append(attr_name)

    return final_list

#############################################################################

def pointFloat(node_relative_path):
    node = hou.pwd()
    input_node = node.node(node_relative_path)
    geo = input_node.geometry()
    final_list = []

    if geo:
        point_attrs_tuple = geo.pointAttribs()
        point_float_attrs_list = []

        for point_attr in point_attrs_tuple:
            if point_attr.size() == 1 and not point_attr.isArrayType():
                if point_attr.dataType().name() == "Float":
                    name = point_attr.name()
                    point_float_attrs_list.append(name)

        point_float_attrs_list.sort()

        for attr_name in point_float_attrs_list:
            final_list.append(attr_name)
            final_list.append(attr_name)

    return final_list

def pointInt(node_relative_path):
    node = hou.pwd()
    input_node = node.node(node_relative_path)
    geo = input_node.geometry()
    final_list = []

    if geo:
        point_attrs_tuple = geo.pointAttribs()
        point_int_attrs_list = []

        for point_attr in point_attrs_tuple:
            if point_attr.size() == 1 and not point_attr.isArrayType():
                if point_attr.dataType().name() == "Int":
                    name = point_attr.name()
                    point_int_attrs_list.append(name)

        point_int_attrs_list.sort()

        for attr_name in point_int_attrs_list:
            final_list.append(attr_name)
            final_list.append(attr_name)

    return final_list

def pointString(node_relative_path):
    node = hou.pwd()
    input_node = node.node(node_relative_path)
    geo = input_node.geometry()
    final_list = []

    if geo:
        point_attrs_tuple = geo.pointAttribs()
        point_string_attrs_list = []

        for point_attr in point_attrs_tuple:
            if point_attr.size() == 1 and not point_attr.isArrayType():
                if point_attr.dataType().name() == "String":
                    name = point_attr.name()
                    point_string_attrs_list.append(name)

        point_string_attrs_list.sort()

        for attr_name in point_string_attrs_list:
            final_list.append(attr_name)
            final_list.append(attr_name)

    return final_list


def pointVector2(node_relative_path):
    node = hou.pwd()
    input_node = node.node(node_relative_path)
    geo = input_node.geometry()
    final_list = []

    if geo:
        point_attrs_tuple = geo.pointAttribs()
        point_vector2_attrs_list = []

        for point_attr in point_attrs_tuple:
            if point_attr.size() == 2 and not point_attr.isArrayType():
                name = point_attr.name()
                point_vector2_attrs_list.append(name)

        point_vector2_attrs_list.sort()

        for attr_name in point_vector2_attrs_list:
            final_list.append(attr_name)
            final_list.append(attr_name)

    return final_list


def pointVector(node_relative_path):
    node = hou.pwd()
    input_node = node.node(node_relative_path)
    geo = input_node.geometry()
    final_list = []

    if geo:
        point_attrs_tuple = geo.pointAttribs()
        point_vector_attrs_list = []

        for point_attr in point_attrs_tuple:
            if point_attr.size() == 3 and not point_attr.isArrayType():
                name = point_attr.name()
                point_vector_attrs_list.append(name)

        point_vector_attrs_list.sort()

        for attr_name in point_vector_attrs_list:
            final_list.append(attr_name)
            final_list.append(attr_name)

    return final_list

def pointVector4(node_relative_path):
    node = hou.pwd()
    input_node = node.node(node_relative_path)
    geo = input_node.geometry()
    final_list = []

    if geo:
        point_attrs_tuple = geo.pointAttribs()
        point_vector4_attrs_list = []

        for point_attr in point_attrs_tuple:
            if point_attr.size() == 4 and not point_attr.isArrayType():
                name = point_attr.name()
                point_vector4_attrs_list.append(name)

        point_vector4_attrs_list.sort()

        for attr_name in point_vector4_attrs_list:
            final_list.append(attr_name)
            final_list.append(attr_name)

    return final_list

################################################################

def primFloat(node_relative_path):
    node = hou.pwd()
    input_node = node.node(node_relative_path)
    geo = input_node.geometry()
    final_list = []

    if geo:
        prim_attrs_tuple = geo.primAttribs()
        prim_float_attrs_list = []

        for prim_attr in prim_attrs_tuple:
            if prim_attr.size() == 1 and not prim_attr.isArrayType():
                if prim_attr.dataType().name() == "Float":
                    name = prim_attr.name()
                    prim_float_attrs_list.append(name)

        prim_float_attrs_list.sort()

        for attr_name in prim_float_attrs_list:
            final_list.append(attr_name)
            final_list.append(attr_name)

    return final_list

def primInt(node_relative_path):
    node = hou.pwd()
    input_node = node.node(node_relative_path)
    geo = input_node.geometry()
    final_list = []

    if geo:
        prim_attrs_tuple = geo.primAttribs()
        prim_int_attrs_list = []

        for prim_attr in prim_attrs_tuple:
            if prim_attr.size() == 1 and not prim_attr.isArrayType():
                if prim_attr.dataType().name() == "Int":
                    name = prim_attr.name()
                    prim_int_attrs_list.append(name)

        prim_int_attrs_list.sort()

        for attr_name in prim_int_attrs_list:
            final_list.append(attr_name)
            final_list.append(attr_name)

    return final_list

def primString(node_relative_path):
    node = hou.pwd()
    input_node = node.node(node_relative_path)
    geo = input_node.geometry()
    final_list = []

    if geo:
        prim_attrs_tuple = geo.primAttribs()
        prim_str_attrs_list = []

        for prim_attr in prim_attrs_tuple:
            if prim_attr.size() == 1 and not prim_attr.isArrayType():
                if prim_attr.dataType().name() == "String":
                    name = prim_attr.name()
                    prim_str_attrs_list.append(name)

        prim_str_attrs_list.sort()

        for attr_name in prim_str_attrs_list:
            final_list.append(attr_name)
            final_list.append(attr_name)

    return final_list


def primVector2(node_relative_path):
    node = hou.pwd()
    input_node = node.node(node_relative_path)
    geo = input_node.geometry()
    final_list = []

    if geo:
        prim_attrs_tuple = geo.primAttribs()
        prim_vector2_attrs_list = []

        for prim_attr in prim_attrs_tuple:
            if prim_attr.size() == 2 and not prim_attr.isArrayType():
                name = prim_attr.name()
                prim_vector2_attrs_list.append(name)

        prim_vector2_attrs_list.sort()

        for attr_name in prim_vector2_attrs_list:
            final_list.append(attr_name)
            final_list.append(attr_name)

    return final_list

def primVector(node_relative_path):
    node = hou.pwd()
    input_node = node.node(node_relative_path)
    geo = input_node.geometry()
    final_list = []

    if geo:
        prim_attrs_tuple = geo.primAttribs()
        prim_vector_attrs_list = []

        for prim_attr in prim_attrs_tuple:
            if prim_attr.size() == 3 and not prim_attr.isArrayType():
                name = prim_attr.name()
                prim_vector_attrs_list.append(name)

        prim_vector_attrs_list.sort()

        for attr_name in prim_vector_attrs_list:
            final_list.append(attr_name)
            final_list.append(attr_name)

    return final_list