import dearpygui.dearpygui as dpg

import sys, os
sys.path.insert(1, os.getcwd())

from config.setup import *
from config.settings import Configs
import pdb

from core import node_editor
from core.dragndrop import DragSource, DragSourceContainer


    
class App:

    def __init__(self):

        self.plugin_menu_id = dpg.generate_uuid()
        self.left_panel = dpg.generate_uuid()
        self.center_panel = dpg.generate_uuid()
        self.right_panel = dpg.generate_uuid()
        self.node_editor = node_editor.NodeEditor()
    
        
        #region datasets
        WIDTH = 155
        datasets = {
            data: DragSource(data)
            for data
            in ["FashionMNIST",
                "Caltech101","Caltech256",
                "CIFAR10",
                "Flowers102",
                "SUN397",
                # доработать
                "CarlaStereo",
                "CelebA",
                "Cityscapes",
                "CLEVRClassification",
                "CocoCaptions",
                "EuroSAT",
                "Food101",
                "ImageNet",
                "Dataset from File",]
        }
        self.dataset_container = DragSourceContainer("Датасеты", WIDTH, -300)
        self.dataset_container.add_drag_source(datasets.values())
        #endregion
        
        #region layers
        layers = {
            layer: DragSource(layer)
            for layer
            in ["LazyLinear",
                "LazyConv1d","LazyConv2d","LazyConv3d",
                "Flatten","Concatenate",
                "LazyBatchNorm1d","LazyBatchNorm2d","LazyBatchNorm3d",
                "AvgPool2d","MaxPool2d","AdaptiveAvgPool2d",
                "Dropout"]
         }
        self.layer_container = DragSourceContainer("Слои", WIDTH, -300)
        self.layer_container.add_drag_source(layers.values())
        #endregion
        
        #region activations
        activations = {
            activation: DragSource(activation)
            for activation
            in ["ReLU","Sigmoid","Tanh",]
         }
        self.activation_container = DragSourceContainer("Функции активаций", WIDTH, 0)
        self.activation_container.add_drag_source(activations.values())
        #endregion

        #region architectures
        archs = {
            'LeNet5': DragSource("LeNet5",
                                (
                                    (layers['LazyConv2d'], {'out_channels':6,"kernel_size":5,"stride":1,"padding":3}),(activations['ReLU'], ),
                                    (layers['MaxPool2d'], {"kernel_size":2,"stride":2}),
                                    (layers['LazyConv2d'], {'out_channels':16,"kernel_size":5,"stride":1,"padding":1}),(activations['ReLU'], ),
                                    (layers['MaxPool2d'], {"kernel_size":2,"stride":2}),
                                    (layers['Flatten'], ),
                                    (layers['LazyLinear'], {'out_features':120}), (activations['ReLU'], ),
                                    (layers['LazyLinear'], {'out_features':84}), (activations['ReLU'], ),
                                    (layers['LazyLinear'], {'out_features':10}),
                                ),
                                 ),
            'AlexNet': DragSource("AlexNet",
                                (
                                    (layers['LazyConv2d'], {'out_channels':96,"kernel_size":11,"stride":4,"padding":1, }),(activations['ReLU'], ),
                                    (layers['MaxPool2d'], {"kernel_size":3,"stride":2}),
                                    (layers['LazyConv2d'], {'out_channels':256,"kernel_size":5,"stride":1,"padding":2, }),(activations['ReLU'], ),
                                    (layers['MaxPool2d'], {"kernel_size":3,"stride":2}),
                                    (layers['LazyConv2d'], {'out_channels':384,"kernel_size":3,"stride":1,"padding":1, }),(activations['ReLU'], ),
                                    (layers['LazyConv2d'], {'out_channels':384,"kernel_size":3,"stride":1,"padding":1, }),(activations['ReLU'], ),
                                    (layers['LazyConv2d'], {'out_channels':256,"kernel_size":3,"stride":1,"padding":1, }),(activations['ReLU'], ),
                                    (layers['MaxPool2d'], {"kernel_size":3,"stride":2}),(layers['Flatten'], ),
                                    (layers['LazyLinear'], {'out_features':4096,  }), (activations['ReLU'], ),(layers['Dropout'], {'p':0.5}),
                                    (layers['LazyLinear'], {'out_features':84,  }), (activations['ReLU'], ),(layers['Dropout'], {'p':0.5}),
                                    (layers['LazyLinear'], {'out_features':10,  }),
                                ),
                                 ),
            'VGG-11': DragSource("VGG-11",
                                (
                                    (layers['LazyConv2d'], {'out_channels':16,"kernel_size":3,"stride":1,"padding":1, }),(activations['ReLU'], ),
                                    (layers['MaxPool2d'], {"kernel_size":2,"stride":2}),
                                    (layers['LazyConv2d'], {'out_channels':32,"kernel_size":3,"stride":1,"padding":1, }),(activations['ReLU'], ),
                                    (layers['MaxPool2d'], {"kernel_size":2,"stride":2}),
                                    (layers['LazyConv2d'], {'out_channels':64,"kernel_size":3,"stride":1,"padding":1, }),(activations['ReLU'], ),
                                    (layers['LazyConv2d'], {'out_channels':64,"kernel_size":3,"stride":1,"padding":1, }),(activations['ReLU'], ),
                                    (layers['MaxPool2d'], {"kernel_size":2,"stride":2}),
                                    (layers['LazyConv2d'], {'out_channels':128,"kernel_size":3,"stride":1,"padding":1, }),(activations['ReLU'], ),
                                    (layers['LazyConv2d'], {'out_channels':128,"kernel_size":3,"stride":1,"padding":1, }),(activations['ReLU'], ),
                                    (layers['MaxPool2d'], {"kernel_size":2,"stride":2}),
                                    (layers['LazyConv2d'], {'out_channels':128,"kernel_size":3,"stride":1,"padding":1, }),(activations['ReLU'], ),
                                    (layers['LazyConv2d'], {'out_channels':128,"kernel_size":3,"stride":1,"padding":1, }),(activations['ReLU'], ),
                                    (layers['MaxPool2d'], {"kernel_size":2,"stride":2}),
                                    (layers['Flatten'], ),
                                    (layers['LazyLinear'], {'out_features':120,  }), (activations['ReLU'], ),
                                    (layers['LazyLinear'], {'out_features':84,  }), (activations['ReLU'], ),
                                    (layers['LazyLinear'], {'out_features':10,  }),
                                ),
                                 ),
            'Conv-MLP': DragSource("Conv-MLP",
                                (
                                    (
                                        (layers['LazyConv2d'], {'out_channels':96, 'kernel_size':11, 'stride':4,'padding':0, }),(activations['ReLU'], ),
                                        (layers['LazyConv2d'], {'out_channels':96, 'kernel_size':1, 'stride':1,'padding':0,  }),(activations['ReLU'], ),
                                        (layers['LazyConv2d'], {'out_channels':96, 'kernel_size':1, 'stride':1,'padding':0,  }),(activations['ReLU'], )
                                    ),
                                )),
            
        }
        archs['NiN'] = DragSource("NiN",
                                (
                                    (archs['Conv-MLP'], [{'out_channels':[96, None, 96, None, 96, None], 'kernel_size':[11, None, 1, None, 1], 'stride':[4, None,1,None, 1,None],'padding':[0,None,0,None,0,None]}]),
                                    (layers['MaxPool2d'], {'kernel_size':3, 'stride':2}),
                                    (archs['Conv-MLP'], [{'out_channels':[256, None, 256, None, 256, None], 'kernel_size':[5,None,1,None,1,None], 'stride':[1,None,1,None,1, None],'padding':[2,None,0,None,0,None]}]),
                                    (layers['MaxPool2d'], {'kernel_size':3, 'stride':2}),
                                    (archs['Conv-MLP'], [{'out_channels':[384, None, 384, None, 384, None], 'kernel_size':[3,None,1,None,1,None], 'stride':[1,None,1,None,1, None],'padding':[1,None,0,None,0,None]}]),
                                    (layers['MaxPool2d'], {'kernel_size':3, 'stride':2}),
                                    (layers['Dropout'], {'p':0.5}),
                                    (archs['Conv-MLP'], [{'out_channels':[10, None, 10, None, 10, None], 'kernel_size':[3,None,1,None,1,None], 'stride':[1,None,1,None,1,None],'padding':[1,None,0,None,0,None]}]),
                                    (layers['AdaptiveAvgPool2d'], {'output_size':'[1, 1]'}),(layers['Flatten'],)
                                ))
        archs['Inception'] = DragSource("Inception",
                                (
                                    (   (layers['LazyConv2d'], {'out_channels':64, 'kernel_size':1}), (activations['ReLU'], ) ),
                                    (
                                        (layers['LazyConv2d'], {'out_channels':96, 'kernel_size':1}), (activations['ReLU'], ),
                                        (layers['LazyConv2d'], {'out_channels':128, 'kernel_size':3, 'padding':1}), (activations['ReLU'], )
                                    ),    
                                    (
                                        (layers['LazyConv2d'], {'out_channels':16, 'kernel_size':1}),(activations['ReLU'], ),
                                        (layers['LazyConv2d'], {'out_channels':32, 'kernel_size':5, 'padding':2}), (activations['ReLU'], )
                                    ),
                                    (
                                        (layers['MaxPool2d'], {'kernel_size':3, 'stride':1, "padding":1}),
                                        (layers['LazyConv2d'], {'out_channels':32, 'kernel_size':1}), (activations['ReLU'], )
                                    )
                                ))
        archs['GoogLeNet'] = DragSource("GoogLeNet",
                                (
                                    (layers['LazyConv2d'], {'out_channels':64, 'kernel_size':7, 'stride':2, 'padding':3}), 
                                    (activations['ReLU'], ),
                                    (layers['MaxPool2d'], {'kernel_size':3, 'stride':2, 'padding':1}),
                                    (layers['LazyConv2d'], {'out_channels':64, 'kernel_size':1}), 
                                    (activations['ReLU'], ),
                                    (layers['LazyConv2d'], {'out_channels':192, 'kernel_size':3, 'padding':1}), 
                                    (activations['ReLU'], ),
                                    (layers['MaxPool2d'], {'kernel_size':3, 'stride':2, 'padding':1}),
                                    (archs['Inception'], [{'out_channels': [64, None]}, 
                                                          {'out_channels': [96, None, 128, None]}, 
                                                          {'out_channels': [16, None, 32, None]}, 
                                                          {'out_channels': [None, 32, None]}]),
                                    (layers['Concatenate'], ),
                                    (archs['Inception'], [{'out_channels': [128, None]}, 
                                                          {'out_channels': [128, None, 192, None]}, 
                                                          {'out_channels': [32, None, 96, None]}, 
                                                          {'out_channels': [None, 64, None]}]),
                                    (layers['Concatenate'], ),
                                    (layers['MaxPool2d'], {'kernel_size':3, 'stride':2, 'padding':1}),
                                    (archs['Inception'], [{'out_channels': [192, None]}, 
                                                          {'out_channels': [96, None, 208, None]}, 
                                                          {'out_channels': [16, None, 48, None]}, 
                                                          {'out_channels': [None, 64, None]}]),
                                    (layers['Concatenate'], ),
                                    (archs['Inception'], [{'out_channels': [160, None]}, 
                                                          {'out_channels': [112, None, 224, None]}, 
                                                          {'out_channels': [24, None, 64, None]}, 
                                                          {'out_channels': [None, 64, None]}]),
                                    (layers['Concatenate'], ),
                                    (archs['Inception'], [{'out_channels': [128, None]}, 
                                                          {'out_channels': [128, None, 256, None]}, 
                                                          {'out_channels': [24, None, 64, None]}, 
                                                          {'out_channels': [None, 64, None]}]),
                                    (layers['Concatenate'], ),
                                    (archs['Inception'], [{'out_channels': [112, None]}, 
                                                          {'out_channels': [144, None, 288, None]}, 
                                                          {'out_channels': [32, None, 64, None]}, 
                                                          {'out_channels': [None, 64, None]}]),
                                    (layers['Concatenate'], ),
                                    (archs['Inception'], [{'out_channels': [256, None]}, 
                                                          {'out_channels': [160, None, 320, None]}, 
                                                          {'out_channels': [32, None, 128, None]}, 
                                                          {'out_channels': [None, 128, None]}]),
                                    (layers['Concatenate'], ),
                                    (layers['MaxPool2d'], {'kernel_size':3, 'stride':2, 'padding':1}),    
                                    (archs['Inception'], [{'out_channels': [256, None]}, 
                                                          {'out_channels': [160, None, 320, None]}, 
                                                          {'out_channels': [32, None, 128, None]}, 
                                                          {'out_channels': [None, 128, None]}]),  
                                    (layers['Concatenate'], ),
                                    (archs['Inception'], [{'out_channels': [384, None]}, 
                                                          {'out_channels': [192, None, 384, None]}, 
                                                          {'out_channels': [48, None, 128, None]}, 
                                                          {'out_channels': [None, 128, None]}]),    
                                    (layers['Concatenate'], ),
                                    (layers['AdaptiveAvgPool2d'], {'output_size':'[1, 1]'}),  
                                    (layers['Flatten'], ), 
                                    (layers['LazyLinear'], {'out_features':10}), 
                                   
                                ))
        archs['BN LeNet'] = DragSource('BN LeNet',
                                (
                                    (layers['LazyConv2d'], {'out_channels':6,"kernel_size":5}),(layers['LazyBatchNorm2d'], ),
                                    (activations['Sigmoid'],), (layers['AvgPool2d'], {'kernel_size': 2, 'stride':2}),
                                    (layers['LazyConv2d'], {'out_channels':16,"kernel_size":5}),(layers['LazyBatchNorm2d'], ),
                                    (activations['Sigmoid'],), (layers['AvgPool2d'], {'kernel_size': 2, 'stride':2}),
                                    (layers['Flatten'], ), (layers['LazyLinear'], {'out_features': 120}),(layers['LazyBatchNorm1d'], ), 
                                    (activations['Sigmoid'], ), (layers['LazyLinear'], {'out_features': 84}),(layers['LazyBatchNorm1d'], ),
                                    (activations['Sigmoid'], ), (layers['LazyLinear'], {'out_features': 10})
                                ))
        
        self.archs_container = DragSourceContainer("Модули", WIDTH, 0)
        self.archs_container.add_drag_source(archs.values())
        #endregion

        

        
    def update(self):

        with dpg.mutex():
            dpg.delete_item(self.left_panel, children_only=True)
            self.dataset_container.submit(self.left_panel)
            self.archs_container.submit(self.left_panel)

            dpg.delete_item(self.right_panel, children_only=True)
            self.layer_container.submit(self.right_panel)
            self.activation_container.submit(self.right_panel)

                

    def start(self):
        dpg.set_viewport_title("Deep Learning Constructor")
        dpg.show_viewport()
        
            
        with dpg.window() as main_window:

            with dpg.menu_bar():
                with dpg.menu(label="Файл"):
                    dpg.add_menu_item(label="Открыть", callback=lambda:self.node_editor.callback_file(self.node_editor.open))
                    dpg.add_menu_item(label="Сохранить", callback=lambda:self.node_editor.callback_file(self.node_editor.save))
                    dpg.add_menu_item(label="Сбросить", callback=self.node_editor.clear)

                with dpg.menu(label="Настройки"):
                    dpg.add_menu_item(label="Логирование", check=True, callback=lambda s,check_value,u:Configs.set_logger)
                    with dpg.menu(label="Инструменты"):
                        dpg.add_menu_item(label="Show Metrics", callback=lambda:dpg.show_tool(dpg.mvTool_Metrics))
                        dpg.add_menu_item(label="Show Documentation", callback=lambda:dpg.show_tool(dpg.mvTool_Doc))
                        dpg.add_menu_item(label="Show Debug", callback=lambda:dpg.show_tool(dpg.mvTool_Debug))
                        dpg.add_menu_item(label="Show Style Editor", callback=lambda:dpg.show_tool(dpg.mvTool_Style))
                        dpg.add_menu_item(label="Show Font Manager", callback=lambda:dpg.show_tool(dpg.mvTool_Font))
                        dpg.add_menu_item(label="Show Item Registry", callback=lambda:dpg.show_tool(dpg.mvTool_ItemRegistry))
                        dpg.add_menu_item(label="Show About", callback=lambda:dpg.show_tool(dpg.mvTool_About))
                
                with dpg.menu(tag='menu_message_logger', label='---Сообщения---'):
                    dpg.add_child_window(tag='message_logger', height=200, width=1000)
            
            with dpg.group(tag='panel', horizontal=True):
                # left panel
                with dpg.group(tag=self.left_panel):
                    self.dataset_container.submit(self.left_panel)
                    self.archs_container.submit(self.left_panel) 

                # center panel
                with dpg.group(tag=self.center_panel):
                    self.node_editor.submit(self.center_panel)
                    dpg.add_text(tag='hover_logger', default_value="Текущий элемент: ", 
                                 parent=self.center_panel)

                # right panel
                with dpg.group(tag=self.right_panel):
                    self.layer_container.submit(self.right_panel)
                    self.activation_container.submit(self.right_panel)


            def on_key_la(sender, app_data):
                if dpg.is_key_released(dpg.mvKey_S):
                    self.node_editor.callback_file(self.node_editor.save)
                if dpg.is_key_released(dpg.mvKey_O):
                    self.node_editor.callback_file(self.node_editor.open)

            with dpg.handler_registry():
                dpg.add_key_press_handler(dpg.mvKey_Control, callback=on_key_la)
                    
                              
        dpg.set_primary_window(main_window, True)
        dpg.start_dearpygui()
        

app = App()
app.start()
