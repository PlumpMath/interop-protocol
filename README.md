Interoperability protocol
=========================

The interoperability protocol enables different Personal Clouds to share resources among them via an API, without forcing users to be in the same provider. More generally, the interoperability protocol creates a freely-implementable and generic methodology for allowing Personal Cloud interoperability.

## Prerequisites

Having two Personal Clouds (Personal Cloud 1 and Personal Cloud 2) that wish to interoperate with each other. They must meet the following requirements before using the present specification.

* Once the interoperability process is completed, Personal Clouds must use APIs to access protected resources. In case they do not implement the Storage API proposed in section 5, Personal Cloud 1 must implement an adapter to access Personal Cloud 2 API, and vice versa.

* Personal Cloud 1 must be registered in Personal Cloud 2 and validated as an authorized service in order to obtain its credentials, and vice versa. The method in which Personal Clouds register with each other and agree to cooperate is beyond the scope of this specification.

## Endpoints

The interoperability protocol defines three endpoints that will be detailed below:

* Share. The URL used to present the interoperability proposal to the user and obtain authorization.
* Unshare. The URL used to finish the interoperability agreement.
* Credentials. The URL used to provide the access credentials.

## Interoperability process overview

The interoperability protocol is done in three steps:

1. User A invites User B to its folder located in Personal Cloud A.
2. Personal Cloud A creates the sharing proposal.
3. Personal Cloud A sends the access credentials to Personal Cloud B.

![Interoperability process](https://raw.githubusercontent.com/cloudspaces/interop-protocol/master/images/interop_process.png)

In the figure above we can observe the interoperability process divided in the three steps commented above.

First, a user in Personal Cloud A expresses its intention of sharing a file with a external user (User B). Personal Cloud A will send an email with information about the proposal to the external user. The external user will select its favourite Personal Cloud, in which it has an account, namely Personal Cloud B. 

In the second step, Personal Cloud A will create the sharing proposal and send it to Personal Cloud B, which will require User B to authorize the proposal. The result of the proposal will be returned to Personal Cloud A. 

Finally, Personal Cloud A will hand the access credentials over the Personal Cloud B, granting forthcoming access to the shared resource.

## User invitation

### User sends an invitation

User A wants to share a folder with User B. Therefore, User A goes to Personal Cloud A, selects the folder he/she wants to share, and introduces the email of User B, who will receive an email indicating the intention of User A to share a folder with him/her and a link to a website located on Personal Cloud A.

### The recipient selects its Personal Cloud

User B clicks on the link and is taken to the Personal Cloud A, where it is asked to select its Personal Cloud from a list of services that have an agreement with Personal Cloud A. User B selects Personal Cloud B.

### Creating the sharing proposal

At this time, Personal Cloud A creates the sharing proposal. To create a sharing proposal, Personal Cloud A sends an HTTP request to Personal Cloud B’s share URL. The Personal Cloud B documentation specifies the HTTP method for this request, and HTTP POST is RECOMMENDED.

