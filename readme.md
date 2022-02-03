# Python client for Online S2T Inference Service

To test the different functionality use demo.py

* create a stub using "grpc_urils.get_Stub()"
* User coresponding function to test any RPC
    - Online Decoding -- tests.testOnline(stub)
    - Offline Decoding -- tests.testOffline(stub)
    - Punctutation -- tests.testPunctuation(stub)


Install dependencies using requirement.txt (recommended to create a virtual/conda environment first)-

```$pip install -r requirement.txt```

Run the demo.py for cli -

```$python demo.py ```

Run the UI.py for UI (available for online decoding only)

```$python UI.py ```




