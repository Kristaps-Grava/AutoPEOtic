from matplotlib import pyplot as py
spectra1 = [4949849.0, 4988332.0, 5026700.0, 4959243.0, 5016783.0, 5043833.0, 5029291.0, 5123089.0, 5086503.0, 5143837.0, 5206726.0, 5178522.0, 5306325.0, 5266141.0, 5268676.0, 5381513.0, 5400397.0, 5452690.0, 5510787.0, 5460478.0, 5564263.0, 5657334.0, 5716058.0, 5804420.0, 5851912.0, 5791983.0, 5940994.0, 5891687.0, 6097101.0, 6077626.0, 6106699.0, 6309754.0, 6465211.0, 6615420.0, 7084312.0, 7462895.0, 8032190.0, 8731488.0, 9360440.0, 1.012152e+07, 1.090413e+07, 1.152309e+07, 1.210245e+07, 1.253973e+07, 1.279882e+07, 1.295799e+07, 1.341221e+07, 1.351291e+07, 1.367604e+07, 1.403501e+07, 1.429202e+07, 1.426209e+07, 1.455001e+07, 1.473994e+07, 1.478044e+07, 1.49212e+07, 1.48668e+07, 1.496376e+07, 1.49064e+07, 1.510613e+07, 1.529173e+07, 1.55751e+07, 1.562838e+07, 1.610266e+07, 1.648255e+07, 1.694903e+07, 1.739635e+07, 1.748603e+07, 1.790816e+07, 1.837957e+07, 1.891706e+07, 1.98901e+07, 2.03836e+07, 2.061104e+07, 2.102256e+07, 2.157284e+07, 2.201474e+07, 2.233047e+07, 2.242893e+07, 2.256786e+07, 2.193702e+07, 2.18997e+07, 2.204272e+07, 2.18122e+07, 2.219573e+07, 2.257325e+07, 2.267524e+07, 2.292075e+07, 2.304839e+07, 2.296274e+07, 2.354357e+07, 2.372386e+07, 2.354155e+07, 2.362565e+07, 2.362216e+07, 2.379266e+07, 2.358544e+07, 2.341071e+07, 2.287883e+07, 2.278606e+07, 2.253117e+07, 2.209368e+07, 2.174179e+07, 2.132276e+07, 2.11629e+07, 2.113769e+07, 2.100093e+07, 2.075249e+07, 2.104573e+07, 2.142437e+07, 2.111572e+07, 2.118719e+07, 2.100536e+07, 2.090598e+07, 2.078618e+07, 2.079735e+07, 2.093148e+07, 2.078894e+07, 2.082665e+07, 2.108506e+07, 2.11998e+07, 2.106276e+07, 2.138087e+07, 2.147611e+07, 2.157128e+07, 2.134218e+07, 2.131776e+07, 2.166835e+07, 2.13655e+07, 2.121923e+07, 2.135108e+07, 2.113216e+07, 2.161533e+07, 2.192944e+07, 2.198162e+07, 2.192168e+07, 2.208493e+07, 2.210537e+07, 2.219709e+07, 2.21755e+07, 2.212212e+07, 2.199524e+07, 2.156558e+07, 2.162247e+07, 2.148044e+07, 2.135722e+07, 2.147525e+07, 2.154063e+07, 2.160579e+07, 2.17026e+07, 2.156516e+07, 2.136223e+07, 2.143598e+07, 2.126253e+07, 2.153997e+07, 2.118101e+07, 2.109029e+07, 2.084638e+07, 1.99358e+07, 1.932485e+07, 1.883119e+07, 1.849914e+07, 1.853944e+07, 1.888892e+07, 1.950579e+07, 1.938114e+07, 1.948932e+07, 1.964229e+07, 1.959401e+07, 1.963486e+07, 1.97768e+07, 1.944488e+07, 1.940507e+07, 1.918304e+07, 1.87205e+07, 1.841485e+07, 1.778704e+07, 1.761423e+07, 1.746243e+07, 1.728718e+07, 1.741101e+07, 1.748876e+07, 1.749688e+07, 1.75745e+07, 1.766379e+07, 1.783501e+07, 1.797152e+07, 1.803784e+07, 1.814018e+07, 1.815927e+07, 1.777508e+07, 1.80536e+07, 1.797647e+07, 1.783907e+07, 1.799924e+07, 1.748956e+07, 1.750505e+07, 1.707545e+07, 1.646288e+07, 1.582313e+07, 1.51432e+07, 1.415754e+07, 1.421268e+07, 1.396327e+07, 1.438397e+07, 1.480623e+07, 1.532812e+07, 1.58773e+07, 1.642776e+07, 1.657311e+07, 1.663226e+07, 1.638166e+07, 1.660149e+07, 1.633681e+07, 1.639488e+07, 1.645292e+07, 1.616051e+07, 1.597876e+07, 1.618711e+07, 1.58657e+07, 1.589676e+07, 1.575077e+07, 1.551533e+07, 1.571012e+07, 1.552408e+07, 1.540077e+07, 1.551921e+07, 1.535663e+07, 1.53469e+07, 1.545241e+07, 1.518529e+07, 1.503288e+07, 1.512485e+07, 1.491965e+07, 1.484299e+07, 1.453235e+07, 1.449331e+07, 1.441489e+07, 1.421862e+07, 1.429582e+07, 1.399358e+07, 1.416206e+07, 1.434409e+07, 1.415821e+07, 1.424824e+07, 1.42064e+07, 1.405847e+07, 1.417476e+07, 1.449026e+07, 1.414221e+07, 1.445836e+07, 1.424209e+07, 1.434544e+07, 1.432858e+07, 1.417752e+07, 1.44418e+07, 1.438419e+07, 1.435316e+07, 1.437581e+07, 1.427683e+07, 1.432616e+07, 1.41723e+07, 1.411278e+07, 1.432467e+07, 1.391023e+07, 1.389047e+07, 1.417165e+07, 1.383667e+07, 1.402248e+07, 1.397392e+07, 1.378862e+07, 1.415354e+07, 1.378779e+07, 1.383544e+07, 1.395215e+07, 1.368179e+07, 1.389532e+07, 1.388738e+07, 1.379595e+07, 1.382933e+07, 1.376516e+07, 1.370069e+07, 1.385941e+07, 1.37247e+07, 1.37856e+07, 1.373433e+07, 1.372495e+07, 1.375761e+07]

spectra2 = [6961, 7953, 8354, 8962, 9602, 10242, 10530, 10946, 11362, 11698, 12066, 12387, 12675, 12899, 12931, 13059, 13267, 13363, 13539, 13699, 13827, 13987, 14099, 14163, 14003, 14099, 14195, 14259, 14355, 14403, 14467, 14259, 14355, 14291, 14323, 14403, 14467, 14483, 14499, 14531, 14579, 14339, 14355, 14403, 14467, 14499, 14531, 14531, 14547, 14275, 14355, 14371, 14467, 14515, 14499, 14275, 14307, 14339, 14371, 14435, 14467, 14499, 14371, 14275, 14355, 14339, 14403, 14819, 15427, 15987, 16484, 16916, 17332, 17492, 17860, 18148, 18404, 18580, 18772, 18884, 18724, 18836, 18900, 18964, 19012, 19012, 18980, 18996, 18772, 18836, 18852, 18852, 18836, 18836, 18532, 18500, 18484, 18452, 18436, 18404, 18356, 18180, 17924, 17860, 17844, 17812, 17828, 17860, 17876, 17668, 17668, 17748, 17844, 17860, 17908, 17940, 17716, 17812, 17860, 17956, 18052, 18116, 17972, 17924, 17956, 17940, 17956, 17940, 17940, 18052, 17716, 17668, 17572, 17556, 17412, 17300, 17172, 16740, 16612, 16516, 16404, 16291, 16227, 16147, 15811, 15715, 15683, 15635, 15603, 15571, 15539, 15459, 15187, 15187, 15155, 15187, 15155, 15139, 14915, 14915, 14931, 14947, 14947, 14979, 14995, 14739, 14787, 14771, 14803, 14803, 14851, 14851, 14723, 14611, 14643, 14691, 14739, 14755, 14787, 14819, 14643, 14723, 14771, 14819, 14867, 14915, 14723, 14739, 14803, 14867, 14931, 14979, 14995, 15075, 14867, 14883, 14947, 14979, 15027, 15075, 15139, 14915, 14979, 15027, 15043, 15107, 15123, 15139, 14915, 14931, 14995, 15043, 15091, 15123, 15171, 15027, 14947, 14963, 15027, 15091, 15123, 15171, 15059, 15011, 15043, 15107, 15139, 15155, 15187, 15171, 14931, 14995, 15043, 15059, 15123, 15139, 15171, 15139, 14931, 14995, 15043, 15091, 15139, 15187, 14979, 15027, 15091, 15123, 15155, 15219, 15267, 15107, 15075, 15123, 15187, 15251, 15283, 15331, 15379, 15155, 15171, 15235, 15299, 15347, 15411, 15187, 15251, 15283, 15331, 15395, 15427, 15459, 15443, 15235, 15267, 15299, 15331, 15331, 15363, 15315, 14531, 14035, 13619, 13235, 12851, 12531, 11954, 11634]




xVertibas = []
i=0
for vertiba in range(0,288):
    xVertibas.append(i)
    i+=1