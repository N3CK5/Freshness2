import numpy as np

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
        
    # computed by one of the nodes Ne  
    def compute_lambda_e(self, w_e, lambda_e, eta_m, theta_e, ratio_lambda_theta_prime):

        return lambda_e + eta_m * ( np.log(w_e/lambda_e) + np.log(1 + (theta_e/lambda_e)) +  ratio_lambda_theta_prime)
    
    def sending_lambda(self):
        pass
    
    def sending_thetas(self):
        pass
    
    def compute_ratio(self, current_device_id):
        res = 0
        for device in self.devices:
            if device.id != current_device_id:
                res += np.log(1 + (device.lambda_e/device.theta_e))
            else:
                pass
            
        return res
            
            
    def compute_theta_e(self, current_device_id):
        res = 0
        for device in self.devices:
            if device.id != current_device_id:
                res += device.lambda_e
            else:
                pass
            
        return res
    
    def update_theta_e_list(self):
        list_of_theta_e = [device.theta_e for device in devices]
    
    def update_lambda_e_list(self):
        list_of_lambda_e = [device.lambda_e for device in devices]
        
    def run_algorithm(self, iterations, eta = 1):
        
        for m in range(iterations):
            for device in self.devices:
                # Send theta_e(m) of current device to all other devices
                self.update_lambda_e_list = update_lambda_e_list()
                
                # Compute lambda_e_prime and theta_e_prime ratios 
                # and compute new lambda_e(m+1) of current device
                ratio_lambda_theta_prime = self.compute_ratio(device.id)
                lambda_e_current_device = self.compute_lambda_e(w_e = 1, lambda_e = device.lambda_e, eta_m = 1, theta_e = device.theta_e , ratio_lambda_theta_prime = ratio_lambda_theta_prime)
                
                #Send lambda_e(m+1) of current device to all other devices
                self.update_lambda_e_list()
                
                #Compute new theta_e of current device
                device.theta_e = self.compute_theta_e(device.id)
                
                #Compute new p_e of current device
                device.p_e = (device.lambda_e / ( device.lambda_e + device.theta_e ) ) 
