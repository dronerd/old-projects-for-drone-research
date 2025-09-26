#ifndef UUID138451022167632
#define UUID138451022167632

/**
  * RandomForestClassifier(base_estimator=deprecated, bootstrap=True, ccp_alpha=0.0, class_name=RandomForestClassifier, class_weight=None, criterion=gini, estimator=DecisionTreeClassifier(), estimator_params=('criterion', 'max_depth', 'min_samples_split', 'min_samples_leaf', 'min_weight_fraction_leaf', 'max_features', 'max_leaf_nodes', 'min_impurity_decrease', 'random_state', 'ccp_alpha'), max_depth=10, max_features=sqrt, max_leaf_nodes=None, max_samples=None, min_impurity_decrease=0.0, min_samples_leaf=1, min_samples_split=2, min_weight_fraction_leaf=0.0, n_estimators=5, n_jobs=None, num_outputs=3, oob_score=False, package_name=everywhereml.sklearn.ensemble, random_state=None, template_folder=everywhereml/sklearn/ensemble, verbose=0, warm_start=False)
 */
class RandomForestClassifier {
    public:

        /**
         * Predict class from features
         */
        int predict(float *x) {
            int predictedValue = 0;
            size_t startedAt = micros();

            
                    
            uint16_t votes[3] = { 0 };
            uint8_t classIdx = 0;
            float classScore = 0;

            
                tree0(x, &classIdx, &classScore);
                votes[classIdx] += classScore;
            
                tree1(x, &classIdx, &classScore);
                votes[classIdx] += classScore;
            
                tree2(x, &classIdx, &classScore);
                votes[classIdx] += classScore;
            
                tree3(x, &classIdx, &classScore);
                votes[classIdx] += classScore;
            
                tree4(x, &classIdx, &classScore);
                votes[classIdx] += classScore;
            

            // return argmax of votes
            uint8_t maxClassIdx = 0;
            float maxVote = votes[0];

            for (uint8_t i = 1; i < 3; i++) {
                if (votes[i] > maxVote) {
                    maxClassIdx = i;
                    maxVote = votes[i];
                }
            }

            predictedValue = maxClassIdx;

                    

            latency = micros() - startedAt;

            return (lastPrediction = predictedValue);
        }

        
            

            /**
             * Predict class label
             */
            String predictLabel(float *x) {
                return getLabelOf(predict(x));
            }

            /**
             * Get label of last prediction
             */
            String getLabel() {
                return getLabelOf(lastPrediction);
            }

            /**
             * Get label of given class
             */
            String getLabelOf(int8_t idx) {
                switch (idx) {
                    case -1:
                        return "ERROR";
                    
                        case 0:
                            return "leftturn";
                    
                        case 1:
                            return "rightturn";
                    
                        case 2:
                            return "straight";
                    
                    default:
                        return "UNKNOWN";
                }
            }


            /**
             * Get latency in micros
             */
            uint32_t latencyInMicros() {
                return latency;
            }

            /**
             * Get latency in millis
             */
            uint16_t latencyInMillis() {
                return latency / 1000;
            }
            

    protected:
        float latency = 0;
        int lastPrediction = 0;

        
            

        
            
                /**
                 * Random forest's tree #0
                 */
                void tree0(float *x, uint8_t *classIdx, float *classScore) {
                    
                        if (x[95] < 0.05165642686188221) {
                            
                                
                        if (x[45] < 0.507276326417923) {
                            
                                
                        if (x[134] < 0.193976528942585) {
                            
                                
                        if (x[124] < 0.4539085924625397) {
                            
                                
                        *classIdx = 1;
                        *classScore = 94.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 84.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[132] < 0.017529773525893688) {
                            
                                
                        *classIdx = 2;
                        *classScore = 84.0;
                        return;

                            
                        }
                        else {
                            
                                
                        if (x[42] < 0.005684151081368327) {
                            
                                
                        *classIdx = 1;
                        *classScore = 94.0;
                        return;

                            
                        }
                        else {
                            
                                
                        if (x[18] < 0.6382550001144409) {
                            
                                
                        *classIdx = 2;
                        *classScore = 84.0;
                        return;

                            
                        }
                        else {
                            
                                
                        if (x[37] < 0.00446808198466897) {
                            
                                
                        *classIdx = 1;
                        *classScore = 94.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 59.0;
                        return;

                            
                        }

                            
                        }

                            
                        }

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[46] < 0.15659522265195847) {
                            
                                
                        *classIdx = 2;
                        *classScore = 84.0;
                        return;

                            
                        }
                        else {
                            
                                
                        if (x[134] < 0.08396022766828537) {
                            
                                
                        if (x[7] < 0.08118168544024229) {
                            
                                
                        *classIdx = 1;
                        *classScore = 94.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 59.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 84.0;
                        return;

                            
                        }

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[12] < 0.015291444957256317) {
                            
                                
                        if (x[44] < 0.03539128974080086) {
                            
                                
                        *classIdx = 1;
                        *classScore = 94.0;
                        return;

                            
                        }
                        else {
                            
                                
                        if (x[62] < 0.06178705766797066) {
                            
                                
                        *classIdx = 1;
                        *classScore = 94.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 59.0;
                        return;

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[51] < 0.08075449988245964) {
                            
                                
                        if (x[49] < 0.6741863489151001) {
                            
                                
                        if (x[44] < 0.11240516975522041) {
                            
                                
                        *classIdx = 1;
                        *classScore = 94.0;
                        return;

                            
                        }
                        else {
                            
                                
                        if (x[100] < 0.0031264913268387318) {
                            
                                
                        if (x[45] < 0.2774004451930523) {
                            
                                
                        *classIdx = 1;
                        *classScore = 94.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 84.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 84.0;
                        return;

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 1;
                        *classScore = 94.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 59.0;
                        return;

                            
                        }

                            
                        }

                            
                        }

                }
            
        
            
                /**
                 * Random forest's tree #1
                 */
                void tree1(float *x, uint8_t *classIdx, float *classScore) {
                    
                        if (x[62] < 0.004031302174553275) {
                            
                                
                        if (x[69] < 0.15963929891586304) {
                            
                                
                        if (x[90] < 0.13870632648468018) {
                            
                                
                        if (x[42] < 0.02687882073223591) {
                            
                                
                        *classIdx = 1;
                        *classScore = 87.0;
                        return;

                            
                        }
                        else {
                            
                                
                        if (x[25] < 0.539881020784378) {
                            
                                
                        if (x[102] < 0.01991882734000683) {
                            
                                
                        *classIdx = 2;
                        *classScore = 80.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 1;
                        *classScore = 87.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 80.0;
                        return;

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[55] < 0.0270949462428689) {
                            
                                
                        *classIdx = 1;
                        *classScore = 87.0;
                        return;

                            
                        }
                        else {
                            
                                
                        if (x[128] < 0.17486463487148285) {
                            
                                
                        *classIdx = 2;
                        *classScore = 80.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 1;
                        *classScore = 87.0;
                        return;

                            
                        }

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[63] < 0.03961608558893204) {
                            
                                
                        *classIdx = 1;
                        *classScore = 87.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 80.0;
                        return;

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[4] < 0.009748191572725773) {
                            
                                
                        if (x[76] < 0.1876630298793316) {
                            
                                
                        if (x[88] < 0.005660916678607464) {
                            
                                
                        if (x[60] < 0.01076414156705141) {
                            
                                
                        *classIdx = 1;
                        *classScore = 87.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 80.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[101] < 0.05134940333664417) {
                            
                                
                        if (x[85] < 0.006574030499905348) {
                            
                                
                        *classIdx = 1;
                        *classScore = 87.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 70.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[5] < 0.009888831526041031) {
                            
                                
                        *classIdx = 0;
                        *classScore = 70.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 80.0;
                        return;

                            
                        }

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 80.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[52] < 0.03571635112166405) {
                            
                                
                        *classIdx = 2;
                        *classScore = 80.0;
                        return;

                            
                        }
                        else {
                            
                                
                        if (x[124] < 0.5128241330385208) {
                            
                                
                        if (x[115] < 0.07098763436079025) {
                            
                                
                        *classIdx = 1;
                        *classScore = 87.0;
                        return;

                            
                        }
                        else {
                            
                                
                        if (x[54] < 0.40252795070409775) {
                            
                                
                        *classIdx = 2;
                        *classScore = 80.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 70.0;
                        return;

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 80.0;
                        return;

                            
                        }

                            
                        }

                            
                        }

                            
                        }

                }
            
        
            
                /**
                 * Random forest's tree #2
                 */
                void tree2(float *x, uint8_t *classIdx, float *classScore) {
                    
                        if (x[71] < 0.049356913194060326) {
                            
                                
                        if (x[44] < 0.47855961322784424) {
                            
                                
                        if (x[45] < 0.4655040204524994) {
                            
                                
                        if (x[75] < 0.03426663437858224) {
                            
                                
                        if (x[26] < 0.6285705119371414) {
                            
                                
                        *classIdx = 1;
                        *classScore = 87.0;
                        return;

                            
                        }
                        else {
                            
                                
                        if (x[99] < 0.39137002825737) {
                            
                                
                        *classIdx = 1;
                        *classScore = 87.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 85.0;
                        return;

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[34] < 0.06556311808526516) {
                            
                                
                        *classIdx = 0;
                        *classScore = 65.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 85.0;
                        return;

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[84] < 0.004570649471133947) {
                            
                                
                        if (x[19] < 0.018967607524245977) {
                            
                                
                        *classIdx = 0;
                        *classScore = 65.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 85.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[82] < 0.5481933355331421) {
                            
                                
                        *classIdx = 0;
                        *classScore = 65.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 1;
                        *classScore = 87.0;
                        return;

                            
                        }

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[123] < 0.593304842710495) {
                            
                                
                        if (x[62] < 0.044201838434673846) {
                            
                                
                        *classIdx = 1;
                        *classScore = 87.0;
                        return;

                            
                        }
                        else {
                            
                                
                        if (x[122] < 0.08923113718628883) {
                            
                                
                        if (x[28] < 0.020743992179632187) {
                            
                                
                        *classIdx = 2;
                        *classScore = 85.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 1;
                        *classScore = 87.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 65.0;
                        return;

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[61] < 0.0024056776892393827) {
                            
                                
                        if (x[9] < 0.35142310336232185) {
                            
                                
                        *classIdx = 0;
                        *classScore = 65.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 1;
                        *classScore = 87.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 65.0;
                        return;

                            
                        }

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[37] < 0.0036343655083328485) {
                            
                                
                        if (x[91] < 0.2327033430337906) {
                            
                                
                        if (x[95] < 0.001355277607217431) {
                            
                                
                        if (x[12] < 0.0162982027977705) {
                            
                                
                        if (x[46] < 0.03242476936429739) {
                            
                                
                        *classIdx = 2;
                        *classScore = 85.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 1;
                        *classScore = 87.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 85.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[126] < 0.547822292894125) {
                            
                                
                        *classIdx = 2;
                        *classScore = 85.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 65.0;
                        return;

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[132] < 0.02604340948164463) {
                            
                                
                        *classIdx = 2;
                        *classScore = 85.0;
                        return;

                            
                        }
                        else {
                            
                                
                        if (x[13] < 0.010921649634838104) {
                            
                                
                        if (x[92] < 0.6827353537082672) {
                            
                                
                        *classIdx = 0;
                        *classScore = 65.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 1;
                        *classScore = 87.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[54] < 0.06270612555090338) {
                            
                                
                        *classIdx = 1;
                        *classScore = 87.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 85.0;
                        return;

                            
                        }

                            
                        }

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[35] < 0.5420605093240738) {
                            
                                
                        *classIdx = 0;
                        *classScore = 65.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 1;
                        *classScore = 87.0;
                        return;

                            
                        }

                            
                        }

                            
                        }

                }
            
        
            
                /**
                 * Random forest's tree #3
                 */
                void tree3(float *x, uint8_t *classIdx, float *classScore) {
                    
                        if (x[132] < 0.2791029214859009) {
                            
                                
                        if (x[124] < 0.20545139908790588) {
                            
                                
                        if (x[134] < 0.04055442661046982) {
                            
                                
                        if (x[118] < 0.19076205417513847) {
                            
                                
                        if (x[85] < 0.515759713947773) {
                            
                                
                        if (x[59] < 0.12905343621969223) {
                            
                                
                        *classIdx = 1;
                        *classScore = 93.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 65.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 79.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 79.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[42] < 0.015163448639214039) {
                            
                                
                        if (x[71] < 0.07046973332762718) {
                            
                                
                        if (x[131] < 0.06459341943264008) {
                            
                                
                        *classIdx = 1;
                        *classScore = 93.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 65.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 79.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[68] < 0.1035180613398552) {
                            
                                
                        if (x[36] < 0.18177861743606627) {
                            
                                
                        *classIdx = 2;
                        *classScore = 79.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 1;
                        *classScore = 93.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 65.0;
                        return;

                            
                        }

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[127] < 0.2129959836602211) {
                            
                                
                        if (x[54] < 0.07275811955332756) {
                            
                                
                        if (x[113] < 0.18724611774086952) {
                            
                                
                        *classIdx = 2;
                        *classScore = 79.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 1;
                        *classScore = 93.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[52] < 0.3252737373113632) {
                            
                                
                        if (x[43] < 0.028281111270189285) {
                            
                                
                        if (x[76] < 0.283290296792984) {
                            
                                
                        *classIdx = 1;
                        *classScore = 93.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 79.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[125] < 0.02211943082511425) {
                            
                                
                        if (x[89] < 0.26943450421094894) {
                            
                                
                        if (x[34] < 0.14347254484891891) {
                            
                                
                        *classIdx = 2;
                        *classScore = 79.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 65.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 1;
                        *classScore = 93.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 79.0;
                        return;

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 65.0;
                        return;

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 65.0;
                        return;

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[106] < 0.15030310302972794) {
                            
                                
                        if (x[0] < 0.2808411866426468) {
                            
                                
                        if (x[75] < 0.02223483845591545) {
                            
                                
                        *classIdx = 1;
                        *classScore = 93.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 65.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[77] < 0.2204667255282402) {
                            
                                
                        *classIdx = 0;
                        *classScore = 65.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 79.0;
                        return;

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 79.0;
                        return;

                            
                        }

                            
                        }

                }
            
        
            
                /**
                 * Random forest's tree #4
                 */
                void tree4(float *x, uint8_t *classIdx, float *classScore) {
                    
                        if (x[95] < 0.056991005316376686) {
                            
                                
                        if (x[71] < 0.20347776263952255) {
                            
                                
                        if (x[70] < 0.15965428203344345) {
                            
                                
                        if (x[62] < 0.05339362286031246) {
                            
                                
                        *classIdx = 1;
                        *classScore = 88.0;
                        return;

                            
                        }
                        else {
                            
                                
                        if (x[51] < 0.0017878260696306825) {
                            
                                
                        *classIdx = 2;
                        *classScore = 82.0;
                        return;

                            
                        }
                        else {
                            
                                
                        if (x[72] < 0.27806442975997925) {
                            
                                
                        *classIdx = 0;
                        *classScore = 67.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 1;
                        *classScore = 88.0;
                        return;

                            
                        }

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[26] < 0.26309579610824585) {
                            
                                
                        if (x[39] < 0.0035830033011734486) {
                            
                                
                        *classIdx = 1;
                        *classScore = 88.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 67.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 82.0;
                        return;

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[112] < 0.2616415470838547) {
                            
                                
                        if (x[7] < 0.27088113129138947) {
                            
                                
                        *classIdx = 2;
                        *classScore = 82.0;
                        return;

                            
                        }
                        else {
                            
                                
                        if (x[106] < 0.06512455642223358) {
                            
                                
                        *classIdx = 2;
                        *classScore = 82.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 67.0;
                        return;

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[6] < 0.008800005540251732) {
                            
                                
                        *classIdx = 1;
                        *classScore = 88.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 67.0;
                        return;

                            
                        }

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        if (x[13] < 0.04022902995347977) {
                            
                                
                        if (x[92] < 0.0978989377617836) {
                            
                                
                        if (x[110] < 0.09487586840987206) {
                            
                                
                        if (x[51] < 0.011235133511945605) {
                            
                                
                        *classIdx = 1;
                        *classScore = 88.0;
                        return;

                            
                        }
                        else {
                            
                                
                        if (x[11] < 0.02016550349071622) {
                            
                                
                        *classIdx = 0;
                        *classScore = 67.0;
                        return;

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 82.0;
                        return;

                            
                        }

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 67.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 0;
                        *classScore = 67.0;
                        return;

                            
                        }

                            
                        }
                        else {
                            
                                
                        *classIdx = 2;
                        *classScore = 82.0;
                        return;

                            
                        }

                            
                        }

                }
            
        


            
};



static RandomForestClassifier classifier;


#endif