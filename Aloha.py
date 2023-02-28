import numpy as np

class Aloha():
    '''
    Distributed Computation of Policy pi_D Algorithm 1,
    "Distributed Scheduling Algorithms for Optimizing Information Freshness in Wireless Networks" 
    R.Talak, S.Karaman, E.Modiano
    arXiv:1803.06469v1 [cs.IT] 17 Mar 2018 
    '''
    
    def __init__(self, devices, theta_e = 0, lambde_e = 1, p_e = 0.5):
        self.lambda_e = lambda_e
        self.theta_e = len(devices)
        self.p_e = p_e
    
    # computed by one of the nodes Ne  
    def cost_function(self, w_e, lambda_e, eta_m, theta_e):
        lambda_theta_prime_ratios = [] #extracting the lambda_e'/theta_e' ratios for every node e' except for node e (current node calculating)
        return lambda_e + eta_m * ( np.log(w_e/lambda_e) + np.log(1 + (theta_e/lambda_e)) + np.sum(np.log(1 + lambda_theta_prime_ratios)) )
    
    def sending_lambda(self):
        pass
    
    def sending_thetas(self):
        pass
    
    def sayinghi(self, id):
        print("hi, my id is ", id)
