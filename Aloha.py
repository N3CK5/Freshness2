import matplotlib.pyplot as plt
import numpy as np
import math
  
class Aloha():
    '''
    Distributed Computation of Policy pi_D Algorithm 1,
    "Distributed Scheduling Algorithms for Optimizing Information Freshness in Wireless Networks" 
    R.Talak, S.Karaman, E.Modiano
    arXiv:1803.06469v1 [cs.IT] 17 Mar 2018 
    '''
    
    def __init__(self, devices):
        self.devices = devices
        self.list_of_theta_e = []
        self.list_of_lambda_e = []
        self.lambda_plot_list = [[] for i in range(len(devices))]
    
        
    # computed by one of the nodes Ne  
    def compute_lambda_e(self, w_e, lambda_e, eta_m, theta_e, ratio_lambda_theta_prime):

        return lambda_e + eta_m * ( np.log(w_e/lambda_e) + np.log(1 + (theta_e/lambda_e)) +  ratio_lambda_theta_prime)
    
    
    def compute_ratio(self, current_device_id):
        res = 0
        for device in self.devices:
            if device.id != current_device_id:
                res += np.log(1 + (device.lambda_e/device.theta_e))
            else:
                pass
            
        return res
            
    def display_pe(self):
        list_pe = []
        
        for device in self.devices:
            list_pe.append(device.p_e)
        return list_pe
    
    def display_lambda(self):
        list_pe = []
        
        for device in self.devices:
            list_pe.append(device.lambda_e)
        return list_pe
        
    def compute_theta_e(self, current_device_id):
        res = 0
        for device in self.devices:
            if device.id != current_device_id:
                res += device.lambda_e
            else:
                pass
            
        return res
    
    def update_theta_e_list(self):
        self.list_of_theta_e = [device.theta_e for device in self.devices]
    
    def update_lambda_e_list(self):
        self.list_of_lambda_e = [device.lambda_e for device in self.devices]
        
    def run_algorithm(self, iterations, eta):
        print("### RUNNING ALGORITHM ###")
        
        for m in range(iterations):
            
            print("--- ITERATION N°", m)
            device_nb = 0
            
            """for device in self.devices:
                # Send theta_e(m) of current device to all other devices
                self.update_theta_e_list()
                
                # Compute lambda_e_prime and theta_e_prime ratios 
                # and compute new lambda_e(m+1) of current device
                ratio_lambda_theta_prime = self.compute_ratio(device.id)
                
                lambda_e_current_device = self.compute_lambda_e(w_e = device.w_e, lambda_e = device.lambda_e, eta_m = 1, theta_e = device.theta_e , ratio_lambda_theta_prime = ratio_lambda_theta_prime)
                device.lambda_e = lambda_e_current_device 
                
                #Send lambda_e(m+1) of current device to all other devices
                self.update_lambda_e_list()
                
                #Compute new theta_e of current device
                device.theta_e = self.compute_theta_e(device.id)
                
                #Compute new p_e of current device
                device.p_e = (device.lambda_e / ( device.lambda_e + device.theta_e ) )
                
                #for plotting lambda_e's
                print(device.id, device.lambda_e)
                self.lambda_plot_list[device_nb].append(device.lambda_e)
                device_nb += 1"""
            
            for device in self.devices:
                # Send theta_e(m) of current device to all other devices
                self.update_theta_e_list()
                
                # Compute lambda_e_prime and theta_e_prime ratios 
                # and compute new lambda_e(m+1) of current device
                ratio_lambda_theta_prime = self.compute_ratio(device.id)
                
                lambda_e_current_device = self.compute_lambda_e(w_e = device.w_e, lambda_e = device.lambda_e, eta_m = 1, theta_e = device.theta_e , ratio_lambda_theta_prime = ratio_lambda_theta_prime)
                device.lambda_e_iterSuivante = lambda_e_current_device
                
            for device in self.devices:
                device.lambda_e = device.lambda_e_iterSuivante
            #Send lambda_e(m+1) of current device to all other devices
            self.update_lambda_e_list()
                
            for device in self.devices:
                #Compute new theta_e of current device
                device.theta_e = self.compute_theta_e(device.id)
                
                #Compute new p_e of current device
                device.p_e = (device.lambda_e / ( device.lambda_e + device.theta_e ) )
                
                #for plotting lambda_e's
                print(device.id, device.lambda_e)
                self.lambda_plot_list[device_nb].append(device.lambda_e)
                device_nb += 1
                
        
    def plot_lambda(self, iterations):
        # Using Numpy to create an array X
        X = np.arange(0, iterations, 1)
        plt.figure(figsize=(15, 8))
        
        # Plotting both the curves simultaneously
        for y in self.lambda_plot_list:
            plt.plot(X, y)
        
        # Naming the x-axis, y-axis and the whole graph
        plt.xlabel("Iterations")
        plt.ylabel("Lambda_e")
        plt.title("Convergence of lambda e's for a fixed number of iterations")
        
        # Adding legend, which helps us recognize the curve according to it's color
        plt.legend()
        
        # To load the display window
        plt.show()
        plt.savefig('lambda_convergence.png')