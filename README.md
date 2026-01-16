## Dataset Used

### FER-2013 (Facial Expression Recognition Dataset)

The face module uses the **FER-2013 dataset** to learn facial emotional patterns that are later mapped to personality traits.

- Grayscale facial images of size **48 × 48**
- Contains **seven facial emotion classes**:
  - Angry
  - Disgust
  - Fear
  - Happy
  - Sad
  - Surprise
  - Neutral

### Dataset Structure
```text
FER2013/
 ├── train/
 └── test/

```
Note: The FER-2013 dataset does not contain personality labels.
It is used to learn facial emotional patterns, which are subsequently mapped to Big Five personality traits using psychologically motivated correlations.
