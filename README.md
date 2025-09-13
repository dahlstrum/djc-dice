This project was an effort in trying to understand the process of how devices securely boot and attest their device identity.

Utilizing documentation on Device Identifier Composition Engine by TCG I tried to develop a mockup of the process.
https://trustedcomputinggroup.org/wp-content/uploads/DICE-Layering-Architecture-r19_pub.pdf

A mock device generates an RSA key pair to set the private key as the Unique Device Secret.
Then each subsequent boot stage is measured and calculated in order to finalize a Composite Device Identifier that can then be used as evidence for attestation.
