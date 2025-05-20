# How to add swipe gesture in ReactNative app? #

To add swipe gestures for navigating between steps in a **React Native** tutorial guide, you can use the **`react-native-gesture-handler`** or **`react-native-swipe-gestures`** library. Here’s a clean and flexible way to implement it:

---

### ✅ Option 1: Using `react-native-gesture-handler` (recommended for full control)

#### 1. **Install dependencies:**

```bash
npm install react-native-gesture-handler react-native-reanimated
```

Make sure to wrap your root app component with `GestureHandlerRootView`.

#### 2. **Wrap the main view:**

```tsx
// App.tsx or index.js
import { GestureHandlerRootView } from 'react-native-gesture-handler';

export default function App() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <YourTutorialComponent />
    </GestureHandlerRootView>
  );
}
```

#### 3. **Use `PanGestureHandler` for swipe detection:**

```tsx
import React, { useState } from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import { PanGestureHandler } from 'react-native-gesture-handler';

const { width } = Dimensions.get('window');

const tutorialSteps = ['Step 1', 'Step 2', 'Step 3'];

export default function Tutorial() {
  const [stepIndex, setStepIndex] = useState(0);

  const handleGesture = ({ nativeEvent }) => {
    if (nativeEvent.translationX < -50 && stepIndex < tutorialSteps.length - 1) {
      setStepIndex(stepIndex + 1); // Swipe left to next
    } else if (nativeEvent.translationX > 50 && stepIndex > 0) {
      setStepIndex(stepIndex - 1); // Swipe right to previous
    }
  };

  return (
    <PanGestureHandler onGestureEvent={handleGesture} activeOffsetX={[-10, 10]}>
      <View style={styles.container}>
        <Text style={styles.stepText}>{tutorialSteps[stepIndex]}</Text>
      </View>
    </PanGestureHandler>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  stepText: { fontSize: 24, padding: 20 },
});
```

---

### ✅ Option 2: Using `react-native-swipe-gestures` (simpler)

#### 1. **Install the package:**

```bash
npm install react-native-swipe-gestures
```

#### 2. **Implement swipe handler:**

```tsx
import React, { useState } from 'react';
import { Text, View, StyleSheet } from 'react-native';
import GestureRecognizer from 'react-native-swipe-gestures';

const tutorialSteps = ['Step 1', 'Step 2', 'Step 3'];

export default function Tutorial() {
  const [stepIndex, setStepIndex] = useState(0);

  const onSwipeLeft = () => {
    if (stepIndex < tutorialSteps.length - 1) setStepIndex(stepIndex + 1);
  };

  const onSwipeRight = () => {
    if (stepIndex > 0) setStepIndex(stepIndex - 1);
  };

  return (
    <GestureRecognizer onSwipeLeft={onSwipeLeft} onSwipeRight={onSwipeRight} style={styles.container}>
      <Text style={styles.text}>{tutorialSteps[stepIndex]}</Text>
    </GestureRecognizer>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  text: { fontSize: 24 },
});
```

---

### 👉 Bonus Tips:

* Add smooth animations between steps using `react-native-reanimated` or `Animated`.
* Prevent overswiping by checking index bounds.
* You could also use a pager view (`react-native-pager-view`) if you're building something like a carousel or onboarding flow.

Would you like me to add animated transitions or page indicators (like dots) as well?
