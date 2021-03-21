package usmb.info802.SOAPLivraison;

import javax.jws.WebMethod;
import javax.jws.WebService;
import javax.jws.soap.SOAPBinding;

@WebService
@SOAPBinding(style = SOAPBinding.Style.RPC)
public class DeliveryCost {
    static final double PRICEPERKGPERKM = 0.1;

    @WebMethod
    public double getDeliveryCost(double distance, double weight) {
        if(distance<0 || weight <0){
            return 0;
        }
        double result = distance * weight * PRICEPERKGPERKM;
        System.out.println(result);
        return result;
    }
}
