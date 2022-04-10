import { Title, Text, Button, Container, Group } from "@mantine/core";
import { useNavigate } from "react-router-dom";

const NotFound = () => {
  const navigate = useNavigate();
  return (
    <Container>
      <Title style={{ fontSize: 150 }}>
        <Text inherit color="red">
          404
        </Text>
      </Title>
      <Title>
        <Text inherit color="red">
          You have found a secret place.
        </Text>
      </Title>
      <Text color="dimmed" size="lg" align="center" mx="xl" px="xl">
        Unfortunately, this is only a 404 page. You may have mistyped the
        address, or the page has been moved to another URL.
      </Text>
      <Group position="center">
        <Button variant="subtle" size="md" onClick={() => navigate(-1)}>
          Take me back
        </Button>
      </Group>
    </Container>
  );
};

export default NotFound;
