Interoperability protocol
=========================

The interoperability protocol enables different Personal Clouds to share resources among them via an API, without forcing users to be in the same provider. More generally, the interoperability protocol creates a freely-implementable and generic methodology for allowing Personal Cloud interoperability.

# Prerequisites

Having two Personal Clouds (Personal Cloud 1 and Personal Cloud 2) that wish to interoperate with each other. They must meet the following requirements before using the present specification.

* Once the interoperability process is completed, Personal Clouds must use APIs to access protected resources. In case they do not implement the Storage API proposed in section 5, Personal Cloud 1 must implement an adapter to access Personal Cloud 2 API, and vice versa.

* Personal Cloud 1 must be registered in Personal Cloud 2 and validated as an authorized service in order to obtain its credentials, and vice versa. The method in which Personal Clouds register with each other and agree to cooperate is beyond the scope of this specification.

# Endpoints

The interoperability protocol defines three endpoints that will be detailed below:

* Share. The URL used to present the interoperability proposal to the user and obtain authorization.
* Unshare. The URL used to finish the interoperability agreement.
* Credentials. The URL used to provide the access credentials.

# Interoperability process overview

The interoperability protocol is done in three steps:

1. User A invites User B to its folder located in Personal Cloud A.
2. Personal Cloud A creates the sharing proposal.
3. Personal Cloud A sends the access credentials to Personal Cloud B.

![Interoperability process](https://raw.githubusercontent.com/cloudspaces/interop-protocol/master/images/interop_process.png)
